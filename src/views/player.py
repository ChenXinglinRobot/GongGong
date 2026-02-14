"""
播放器视图模块
包含核心播放器逻辑，使用 Stack 分层架构实现无遮挡交互
"""

import flet as ft
import flet_video as ftv
import asyncio
from typing import List
from data_loader import Topic, Question
import utils
import config


def create_glass_button(text, icon, color, on_click_handler, expand=True, will_be_replaced=False):
    """
    创建有色毛玻璃按钮 (Tinted Glass)
    will_be_replaced: 如果为True，表示按钮在点击后会被替换，不需要恢复状态
    """
    import asyncio

    # 颜色定义
    normal_bg = ft.Colors.with_opacity(0.35, color)
    hover_bg = ft.Colors.with_opacity(0.5, color)
    pressed_bg = ft.Colors.with_opacity(0.7, color)
    border_color = ft.Colors.with_opacity(0.3, ft.Colors.WHITE)
    hover_border_color = ft.Colors.with_opacity(0.6, ft.Colors.WHITE)

    # 点击事件包装器
    async def wrapped_on_click(e):
        # 按下效果
        btn_container.bgcolor = pressed_bg
        btn_container.scale = 0.96
        btn_container.update()
        await asyncio.sleep(0.05)  # 短暂延迟，让用户感受到按下效果
        
        # 切换到悬停状态
        btn_container.bgcolor = hover_bg
        btn_container.scale = 1.0
        btn_container.border = ft.Border.all(1.5, hover_border_color)
        btn_container.update()
        await asyncio.sleep(0.05)
        
        # 执行业务逻辑
        if on_click_handler:
            if asyncio.iscoroutinefunction(on_click_handler):
                await on_click_handler(e)
            else:
                on_click_handler(e)
        
        # 🔥 智能状态恢复：只有按钮不会被替换时才恢复状态
        if not will_be_replaced:
            try:
                if btn_container.page:  # 检查按钮是否还在页面上
                    btn_container.bgcolor = normal_bg
                    btn_container.scale = 1.0
                    btn_container.border = ft.Border.all(1.5, border_color)
                    btn_container.update()
            except Exception:
                # 如果按钮已被移除或替换，忽略错误
                pass

    # 容器定义
    btn_container = ft.Container(
        content=ft.Row(
            [
                ft.Icon(icon, color=ft.Colors.WHITE, size=20),
                ft.Text(text, color=ft.Colors.WHITE, size=16, weight="w500") 
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        ),
        padding=ft.Padding.symmetric(horizontal=20, vertical=18),
        border_radius=12,
        bgcolor=normal_bg,
        blur=ft.Blur(15, 15, ft.BlurTileMode.CLAMP),
        border=ft.Border.all(1.5, border_color),
        shadow=ft.BoxShadow(
            spread_radius=0,
            blur_radius=10,
            color=ft.Colors.BLACK_26, 
            offset=ft.Offset(0, 4),
        ),
        clip_behavior=ft.ClipBehavior.HARD_EDGE, 
        animate=ft.Animation(100, ft.AnimationCurve.EASE_OUT),
        on_click=wrapped_on_click,
    )
    
    if expand:
        btn_container.expand = True
    
    def on_tap_down(e):
        btn_container.bgcolor = pressed_bg
        btn_container.scale = 0.96
        btn_container.update()
    
    def on_hover(e):
        is_hovering = e.data == "true"
        btn_container.bgcolor = hover_bg if is_hovering else normal_bg
        current_border = hover_border_color if is_hovering else border_color
        btn_container.border = ft.Border.all(1.5, current_border)
        btn_container.scale = 1.0
        btn_container.update()

    btn_container.on_tap_down = on_tap_down
    btn_container.on_hover = on_hover
    
    return btn_container


def get_player_view(page: ft.Page, topic: Topic):
    """核心播放页面 - 修复层级遮挡与交互逻辑"""
    current_q_index = 0
    questions: List[Question] = topic.questions
    total_questions = len(questions)

    # 状态变量
    overlay_visible = False
    
    # 🔥 核心修正：使用 is_paused 变量，逻辑更清晰
    is_paused = False # 默认自动播放，所以初始不是暂停状态
    
    auto_hide_task = None
    
    # 添加标志以忽略视频加载后的首次完成事件
    ignore_first_completion = True

    # --- Logic Functions ---

    async def update_ui_state(state_id: int):
        nonlocal current_q_index
        if current_q_index >= total_questions:
            return

        q = questions[current_q_index]
        raw_path = q.videos.get(state_id)
        
        if raw_path:
            src = utils.get_video_src(raw_path)
            
            new_player = ftv.Video(
                expand=True,
                autoplay=True,
                show_controls=False,
                playlist=[ftv.VideoMedia(src)],
                fit=ft.BoxFit.CONTAIN,
                filter_quality=ft.FilterQuality.MEDIUM,
                key=f"video_{q.id}_{state_id}_{current_q_index}",
                on_complete=on_video_completed
            )
            video_container.content = new_player
        else:
            video_container.content = ft.Text("视频缺失", color=config.COLOR_TEXT_ERROR)

        # 🔥 关键修复：每次状态切换都重新创建按钮
        controls_row.controls.clear()
        controls_row.controls = create_buttons_for_state(state_id)

        # 视频切换：重置为播放状态 (is_paused = False)
        nonlocal is_paused, ignore_first_completion
        is_paused = False
        ignore_first_completion = True  # 重置标志，忽略新视频的首次完成事件
        print(f"[UI UPDATE] Switching to State {state_id}. is_paused reset to False. Reset ignore_first_completion")
        
        # 立即更新中央按钮（确保它隐藏）
        update_central_button_visuals()
        
        # 显示菜单，并启动自动隐藏
        await show_overlay()
        await start_auto_hide()
        
        page.update()
    
    # --- 事件处理 ---
    
    async def on_repeat_click(e): await update_ui_state(1)
    async def on_forget_click(e): await update_ui_state(3)
    async def on_correct_click(e): await update_ui_state(2)
    async def on_retry_click(e): await update_ui_state(0)
    
    async def on_next_or_skip_click(e):
        nonlocal current_q_index
        if current_q_index < total_questions - 1:
            current_q_index += 1
            title_text.value = f"当前进度: {current_q_index + 1} / {total_questions}"
            await update_ui_state(0)
    
    async def on_finish_click(e): 
        video_container.content = None 
        await page.push_route("/")

    async def on_back_nav_click(e): 
        video_container.content = None
        await page.push_route("/")
    
    # --- 控制逻辑 ---

    def update_central_button_visuals():
        """
        更新中央大按钮
        逻辑：只有当【暂停】时才显示，【播放】时必须隐藏
        """
        print(f"[VISUAL] Updating Button. is_paused={is_paused} -> Button Visible Should be {is_paused}")
        if is_paused:
            # 暂停中 -> 显示按钮
            central_play_btn.visible = True
            central_play_btn.opacity = 1
            central_play_btn.scale = 1.0
        else:
            # 正在播放 -> 隐藏按钮
            central_play_btn.opacity = 0
            central_play_btn.scale = 0.8
            central_play_btn.visible = False # 彻底隐藏
        
        central_play_btn.update()

    async def toggle_play_pause(e):
        """切换播放/暂停"""
        if video_container.content:
            await video_container.content.play_or_pause()
            nonlocal is_paused
            is_paused = not is_paused # 状态翻转
            print(f"[ACTION] Toggle Play/Pause. New state: is_paused={is_paused}")
            
            update_central_button_visuals()
            
            if is_paused:
                # 暂停状态：直接显示菜单，取消自动隐藏
                await show_overlay()
                if auto_hide_task:
                    auto_hide_task.cancel()
            else:
                # 播放状态：直接显示菜单并启动5秒后自动隐藏
                await show_overlay()
                await start_auto_hide()
    
    async def handle_screen_tap(e):
        """单击屏幕空白处：切换菜单显示"""
        if overlay_visible:
            await hide_overlay()
        else:
            await show_overlay()
            # 如果是播放状态 (not is_paused)，显示后需要启动倒计时
            if not is_paused:
                await start_auto_hide()

    async def show_overlay():
        nonlocal overlay_visible
        overlay_visible = True
        
        print(f"[SHOW OVERLAY] Starting overlay show animation")
        print(f"  Current state - Top: opacity={top_bar_container.opacity}, offset={top_bar_container.offset}")
        print(f"  Current state - Bottom: opacity={bottom_bar_container.opacity}, offset={bottom_bar_container.offset}")
        
        # 🔥 改进的修复方案：正确比较offset值
        # 检查当前offset值，如果不在隐藏位置，需要修正
        
        # 获取当前offset值，安全处理None情况
        current_top_offset = top_bar_container.offset or ft.Offset(0, 0)
        current_bottom_offset = bottom_bar_container.offset or ft.Offset(0, 0)
        
        # 打印详细的offset信息以便调试
        print(f"  Current top offset: x={current_top_offset.x}, y={current_top_offset.y}")
        print(f"  Target top offset: x=0, y=-1")
        
        # 检查是否需要修正offset（比较x和y值）
        needs_top_correction = abs(current_top_offset.x - 0) > 0.001 or abs(current_top_offset.y - (-1)) > 0.001
        needs_bottom_correction = abs(current_bottom_offset.x - 0) > 0.001 or abs(current_bottom_offset.y - 1) > 0.001
        
        # 如果当前opacity>0（可能是部分显示状态），先设置到完全隐藏
        # 但为了避免闪烁，我们只在必要时调整
        if top_bar_container.opacity > 0.1:
            # 如果opacity较高，说明可能部分可见，需要先完全隐藏
            top_bar_container.opacity = 0
            bottom_bar_container.opacity = 0
            page.update()
            await asyncio.sleep(0.01)  # 短暂延迟
        
        # 确保从正确的offset位置开始动画
        if needs_top_correction:
            print(f"  Correcting top offset from ({current_top_offset.x}, {current_top_offset.y}) to (0, -1)")
            # 保存当前动画设置
            original_top_animate = top_bar_container.animate_offset
            # 临时禁用动画，快速设置到正确起始位置
            top_bar_container.animate_offset = None
            top_bar_container.offset = ft.Offset(0, -1)
            # 立即恢复动画设置
            top_bar_container.animate_offset = original_top_animate
            page.update()
            await asyncio.sleep(0.02)  # 给UI足够时间处理
        
        if needs_bottom_correction:
            print(f"  Correcting bottom offset from ({current_bottom_offset.x}, {current_bottom_offset.y}) to (0, 1)")
            # 保存当前动画设置
            original_bottom_animate = bottom_bar_container.animate_offset
            # 临时禁用动画，快速设置到正确起始位置
            bottom_bar_container.animate_offset = None
            bottom_bar_container.offset = ft.Offset(0, 1)
            # 立即恢复动画设置
            bottom_bar_container.animate_offset = original_bottom_animate
            page.update()
            await asyncio.sleep(0.02)
        
        # 设置目标状态，开始500ms动画
        top_bar_container.opacity = 1
        top_bar_container.offset = ft.Offset(0, 0)
        bottom_bar_container.opacity = 1
        bottom_bar_container.offset = ft.Offset(0, 0)
        
        page.update()
        print(f"[SHOW OVERLAY] Animation started from correct positions")
    
    async def hide_overlay():
        nonlocal overlay_visible
        overlay_visible = False
        
        # 顶部栏：上滑隐藏 (0, -1)
        top_bar_container.opacity = 0
        top_bar_container.offset = ft.Offset(0, -1)
        
        # 底部栏：下滑隐藏 (0, 1)
        bottom_bar_container.opacity = 0
        bottom_bar_container.offset = ft.Offset(0, 1)
        
        page.update()
    
    async def start_auto_hide():
        """启动自动隐藏任务"""
        nonlocal auto_hide_task
        if auto_hide_task:
            auto_hide_task.cancel()
        
        print(f"[TIMER] Attempting start auto-hide. is_paused={is_paused}, overlay={overlay_visible}")
        
        # 🔥 修正逻辑：只有在播放时 (not is_paused) 才启动自动隐藏任务
        if not is_paused:
            async def auto_hide_task_func():
                await asyncio.sleep(5)
                # 再次检查状态，确保仍然是播放状态且菜单可见
                if not is_paused and overlay_visible:
                    await hide_overlay()
            
            auto_hide_task = asyncio.create_task(auto_hide_task_func())
        else:
            print("[TIMER] Skipping auto-hide because video is paused")

    async def on_video_completed(e):
        """播放结束"""
        nonlocal is_paused, ignore_first_completion
        
        # 如果这是视频加载后的首次完成事件，忽略它
        if ignore_first_completion:
            print(f"[EVENT] Ignoring first completion event. is_paused={is_paused}")
            ignore_first_completion = False
            return
            
        print(f"[EVENT] Video Completed. Current is_paused={is_paused}, Setting to True")
        is_paused = True # 播放结束视为暂停
        
        # 显示大按钮
        update_central_button_visuals()
        
        # 🔥 特殊处理视频完成时的动画：强制确保从正确位置开始
        print(f"[EVENT] Before show_overlay - Top offset: {top_bar_container.offset}, Bottom offset: {bottom_bar_container.offset}")
        
        # 方案：先无动画地强制设置到隐藏位置，然后立即显示
        # 保存当前动画设置
        original_top_animate_offset = top_bar_container.animate_offset
        original_top_animate_opacity = top_bar_container.animate_opacity
        original_bottom_animate_offset = bottom_bar_container.animate_offset
        original_bottom_animate_opacity = bottom_bar_container.animate_opacity
        
        # 临时禁用所有动画
        top_bar_container.animate_offset = None
        top_bar_container.animate_opacity = None
        bottom_bar_container.animate_offset = None
        bottom_bar_container.animate_opacity = None
        
        # 强制设置到隐藏位置
        top_bar_container.opacity = 0
        top_bar_container.offset = ft.Offset(0, -1)
        bottom_bar_container.opacity = 0
        bottom_bar_container.offset = ft.Offset(0, 1)
        
        # 立即更新
        page.update()
        await asyncio.sleep(0.02)  # 短暂延迟确保状态更新
        
        # 恢复动画设置
        top_bar_container.animate_opacity = original_top_animate_opacity
        top_bar_container.animate_offset = original_top_animate_offset
        bottom_bar_container.animate_opacity = original_bottom_animate_opacity
        bottom_bar_container.animate_offset = original_bottom_animate_offset
        
        # 现在调用 show_overlay()，它会从正确的隐藏位置开始动画
        await show_overlay()

    # --- UI Elements ---

    # 按钮创建函数 - 在 update_ui_state 中动态创建
    def create_buttons_for_state(state_id):
        """根据状态创建对应的按钮组"""
        if state_id == 0 or state_id == 1:
            # State 0 和 1 使用相同的按钮组
            # "听不清"按钮不会被替换（同一状态内），其他按钮会被替换
            return [
                create_glass_button("听不清 / 再说一遍", ft.Icons.HEARING, config.COLOR_BTN_REPEAT, on_repeat_click, will_be_replaced=False),
                create_glass_button("忘记了", ft.Icons.HELP_OUTLINE, config.COLOR_BTN_FORGET, on_forget_click, will_be_replaced=True),
                create_glass_button("回答正确", ft.Icons.CHECK_CIRCLE, config.COLOR_BTN_CORRECT, on_correct_click, will_be_replaced=True)
            ]
        elif state_id == 2:
            if current_q_index < total_questions - 1:
                return [create_glass_button("下一题", ft.Icons.ARROW_FORWARD, config.COLOR_BTN_NEXT, on_next_or_skip_click, will_be_replaced=True)]
            else:
                return [create_glass_button("完成 - 返回菜单", ft.Icons.HOME, config.COLOR_BTN_FINISH, on_finish_click, will_be_replaced=True)]
        elif state_id == 3:
            return [
                create_glass_button("重试本题", ft.Icons.REFRESH, config.COLOR_BTN_RETRY, on_retry_click, will_be_replaced=True),
                create_glass_button("跳过", ft.Icons.SKIP_NEXT, config.COLOR_BTN_SKIP, on_next_or_skip_click, will_be_replaced=True)
            ]
        return []

    controls_row = ft.Row(
        spacing=15,
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    title_text = ft.Text(f"当前进度: 1 / {total_questions}", size=config.TEXT_SIZE_SMALL, color=config.COLOR_TEXT_TITLE)
    
    # Layer 1: 视频容器
    video_container = ft.Container(
        bgcolor=config.COLOR_BG_BLACK,
        alignment=ft.Alignment(0, 0),
        content=ft.ProgressRing()
    )

    # Layer 2: 全屏手势层
    gesture_layer = ft.GestureDetector(
        expand=True,
        on_tap=handle_screen_tap,        # 单击显隐菜单
        on_double_tap=toggle_play_pause, # 双击暂停/播放
        content=ft.Container(bgcolor=ft.Colors.TRANSPARENT, expand=True) # 透明实体填充
    )

    # Layer 3: 中央巨型播放按钮 (Central Play Button)
    central_play_btn = ft.Container(
        content=ft.Icon(ft.Icons.PLAY_ARROW_ROUNDED, size=64, color=ft.Colors.WHITE),
        width=100, height=100,
        alignment=ft.Alignment.CENTER,
        bgcolor=ft.Colors.with_opacity(0.4, ft.Colors.BLACK),
        blur=ft.Blur(20, 20, ft.BlurTileMode.CLAMP),
        shape=ft.BoxShape.CIRCLE,
        border=ft.Border.all(2, ft.Colors.with_opacity(0.5, ft.Colors.WHITE)),
        # 初始状态：播放中(is_paused=False) -> 隐藏
        opacity=0, 
        scale=0.8,
        visible=False,
        animate_opacity=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
        animate_scale=ft.Animation(300, ft.AnimationCurve.EASE_OUT_BACK),
        on_click=toggle_play_pause, 
    )

    # Layer 4: 顶部栏 (Top Bar)
    top_bar_container = ft.Container(
        top=0, left=0, right=0, # 绝对定位
        bgcolor=config.COLOR_BG_TRANSPARENT,
        padding=ft.Padding.only(top=20, left=15, right=15, bottom=10),
        content=ft.Row(
            [
                ft.IconButton(ft.Icons.ARROW_BACK, on_click=on_back_nav_click, icon_color=config.COLOR_TEXT_WHITE, icon_size=40),
                ft.Column(
                    [
                        ft.Text(topic.name, color=config.COLOR_TEXT_WHITE, size=config.TEXT_SIZE_MEDIUM, weight=ft.FontWeight.BOLD),
                        title_text
                    ],
                    spacing=2
                ),
                ft.Container(expand=True)
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        ),
        opacity=0,
        offset=ft.Offset(0, -1), 
        animate_opacity=ft.Animation(500, ft.AnimationCurve.EASE_OUT_CUBIC),
        animate_offset=ft.Animation(500, ft.AnimationCurve.EASE_OUT_CUBIC),
    )

    # Layer 5: 底部栏 (Bottom Bar)
    bottom_bar_container = ft.Container(
        bottom=0, left=0, right=0, # 绝对定位
        padding=20,
        content=controls_row,
        opacity=0,
        offset=ft.Offset(0, 1), 
        animate_opacity=ft.Animation(500, ft.AnimationCurve.EASE_OUT_CUBIC),
        animate_offset=ft.Animation(500, ft.AnimationCurve.EASE_OUT_CUBIC),
    )

    # --- Final Stack ---
    stack_layers = ft.Stack(
        expand=True,
        alignment=ft.Alignment.CENTER, 
        controls=[
            video_container,      # Layer 1
            gesture_layer,        # Layer 2
            central_play_btn,     # Layer 3
            top_bar_container,    # Layer 4
            bottom_bar_container, # Layer 5
        ]
    )

    # --- Initialization ---
    if total_questions > 0:
        first_q = questions[0]
        if 0 in first_q.videos:
            init_src = utils.get_video_src(first_q.videos[0])
            video_container.content = ftv.Video(
                expand=True,
                autoplay=True,
                show_controls=False,
                playlist=[ftv.VideoMedia(init_src)],
                fit=ft.BoxFit.CONTAIN,
                filter_quality=ft.FilterQuality.MEDIUM,
                on_complete=on_video_completed
            )
        
        # 🔥 初始化时也使用新的按钮创建逻辑
        controls_row.controls = create_buttons_for_state(0)
        
        # 初始化状态同步：确保中间按钮隐藏 (因为默认自动播放)
        central_play_btn.visible = False
        
        try:
            asyncio.create_task(start_auto_hide())
        except RuntimeError:
            pass

    return ft.View(
        route=f"/play/{topic.id}",
        padding=0,
        controls=[stack_layers]
    )