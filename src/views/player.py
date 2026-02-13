"""
播放器视图模块
包含核心播放器逻辑，使用 Stack 三层架构实现沉浸式覆盖
"""

import flet as ft
import flet_video as ftv
from typing import List
from data_loader import Topic, Question
import utils
import config


def create_glass_button(text, icon, color, on_click_handler, expand=True):
    """
    创建有色毛玻璃按钮 (Tinted Glass) - 终极交互修复版
    修复问题：
    1. 按钮颜色卡在"深色"状态
    2. 需要点击两次才能触发
    """
    import asyncio # 确保引入 asyncio

    # 颜色定义
    normal_bg = ft.Colors.with_opacity(0.35, color)
    hover_bg = ft.Colors.with_opacity(0.5, color)
    pressed_bg = ft.Colors.with_opacity(0.7, color)
    border_color = ft.Colors.with_opacity(0.3, ft.Colors.WHITE)
    hover_border_color = ft.Colors.with_opacity(0.6, ft.Colors.WHITE)

    # --- 🔥 核心修复逻辑 ---
    async def wrapped_on_click(e):
        """
        点击事件包装器：
        先强制恢复按钮外观，再执行业务逻辑。
        """
        # 1. 强制视觉复位 (Resets Visuals)
        # 无论之前是什么状态，点击发生时，立刻变回"悬停/普通"颜色
        # 并恢复缩放比例
        btn_container.bgcolor = hover_bg
        btn_container.scale = 1.0
        btn_container.border = ft.Border.all(1.5, hover_border_color)
        btn_container.update()
        
        # 2. 视觉延迟 (Visual Delay)
        # 给用户 0.1 秒的时间看到按钮"弹起"的效果
        # 这也是解决"点击无效"的关键，给 UI 线程喘息时间
        await asyncio.sleep(0.1)

        # 3. 执行真正的逻辑 (Execute Logic)
        if on_click_handler:
            if asyncio.iscoroutinefunction(on_click_handler):
                await on_click_handler(e)
            else:
                on_click_handler(e)

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
        animate=ft.Animation(100, ft.AnimationCurve.EASE_OUT), # 动画加快一点，更跟手
        
        # 🔥 关键：使用包装后的点击事件
        on_click=wrapped_on_click,
    )
    
    if expand:
        btn_container.expand = True
    
    # --- 简化的交互逻辑 ---
    # 我们移除了 on_tap_up，因为 wrapped_on_click 已经接管了松手后的逻辑
    # 这样避免了事件冲突
    
    def on_tap_down(e):
        """按下时：变深，缩小"""
        btn_container.bgcolor = pressed_bg
        btn_container.scale = 0.96
        btn_container.update()
    
    def on_hover(e):
        """悬停时：变亮"""
        is_hovering = e.data == "true"
        # 只有在没有按下时才改变颜色
        btn_container.bgcolor = hover_bg if is_hovering else normal_bg
        # 边框变亮
        current_border = hover_border_color if is_hovering else border_color
        btn_container.border = ft.Border.all(1.5, current_border)
        btn_container.scale = 1.0 # 确保鼠标移出时恢复大小
        btn_container.update()

    # 绑定事件
    btn_container.on_tap_down = on_tap_down
    btn_container.on_hover = on_hover
    
    return btn_container

def get_player_view(page: ft.Page, topic: Topic):
    """核心播放页面 - 使用 Stack 三层架构实现沉浸式覆盖"""
    current_q_index = 0
    questions: List[Question] = topic.questions
    total_questions = len(questions)

    # --- Logic Functions (需要在事件处理函数之前定义) ---

    async def update_ui_state(state_id: int):
        nonlocal current_q_index
        if current_q_index >= total_questions:
            return

        q = questions[current_q_index]
        raw_path = q.videos.get(state_id)
        
        if raw_path:
            src = utils.get_video_src(raw_path)
            print(f"Switching video to: {src}")
            
            # 创建新的 Video 组件
            new_player = ftv.Video(
                expand=True,
                autoplay=True,
                show_controls=False,
                playlist=[ftv.VideoMedia(src)],
                fit=ft.BoxFit.CONTAIN,
                filter_quality=ft.FilterQuality.MEDIUM,
                key=f"video_{q.id}_{state_id}_{current_q_index}"
            )
            
            # 将容器内容替换为新播放器
            video_container.content = new_player
        else:
            print(f"Error: Missing video for State {state_id} in Question {q.id}")
            video_container.content = ft.Text("视频缺失", color=config.COLOR_TEXT_ERROR)

        controls_row.controls.clear()

        if state_id == 0 or state_id == 1:
            controls_row.controls = [btn_repeat, btn_forget, btn_correct]
        elif state_id == 2:
            if current_q_index < total_questions - 1:
                controls_row.controls = [btn_next]
            else:
                controls_row.controls = [btn_finish]
        elif state_id == 3:
            controls_row.controls = [btn_retry, btn_skip]

        page.update()
    
    # --- 事件处理函数定义（需要在按钮之前定义）---
    
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
        # 离开前清空视频，防止后台声音
        video_container.content = None 
        await page.push_route("/")

    async def on_back_nav_click(e): 
        video_container.content = None
        await page.push_route("/")
    
    # --- UI Controls Definition ---
    
    # 按钮定义 - 使用毛玻璃效果
    btn_repeat = create_glass_button(
        "听不清 / 再说一遍",
        ft.Icons.HEARING,
        config.COLOR_BTN_REPEAT,
        on_repeat_click,
        expand=True
    )
    
    btn_forget = create_glass_button(
        "忘记了",
        ft.Icons.HELP_OUTLINE,
        config.COLOR_BTN_FORGET,
        on_forget_click,
        expand=True
    )

    btn_correct = create_glass_button(
        "回答正确",
        ft.Icons.CHECK_CIRCLE,
        config.COLOR_BTN_CORRECT,
        on_correct_click,
        expand=True
    )

    btn_next = create_glass_button(
        "下一题",
        ft.Icons.ARROW_FORWARD,
        config.COLOR_BTN_NEXT,
        on_next_or_skip_click,
        expand=True
    )
    
    btn_finish = create_glass_button(
        "完成 - 返回菜单",
        ft.Icons.HOME,
        config.COLOR_BTN_FINISH,
        on_finish_click,
        expand=True
    )

    btn_retry = create_glass_button(
        "重试本题",
        ft.Icons.REFRESH,
        config.COLOR_BTN_RETRY,
        on_retry_click,
        expand=True
    )

    btn_skip = create_glass_button(
        "跳过",
        ft.Icons.SKIP_NEXT,
        config.COLOR_BTN_SKIP,
        on_next_or_skip_click,
        expand=True
    )

    controls_row = ft.Row(
        spacing=15,
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # 进度文本
    title_text = ft.Text(f"当前进度: 1 / {total_questions}", size=config.TEXT_SIZE_SMALL, color=config.COLOR_TEXT_TITLE)
    
    # 视频容器 - 用于动态更新视频
    video_container = ft.Container(
        bgcolor=config.COLOR_BG_BLACK,
        alignment=ft.Alignment(0, 0),  # 居中对齐
        content=ft.ProgressRing()  # 初始显示加载圈
    )
    
    # UI 覆盖层可见性状态
    overlay_visible = False
    
    # --- 手势处理函数 ---
    
    async def toggle_overlay(e):
        nonlocal overlay_visible
        overlay_visible = not overlay_visible
        overlay_container.visible = overlay_visible
        page.update()
    
    async def toggle_play_pause(e):
        # 切换视频播放/暂停（使用官方 API）
        if video_container.content:
            await video_container.content.play_or_pause()
    
    # --- Layer 3: UI 覆盖层 (Top) ---
    # 先创建返回按钮，以便绑定事件
    back_button = ft.IconButton(
        ft.Icons.ARROW_BACK,
        on_click=None,  # 稍后绑定
        icon_color=config.COLOR_TEXT_WHITE
    )
    
    overlay_container = ft.Container(
        left=0,
        top=0,
        right=0,
        bottom=0,
        visible=False,  # 初始隐藏
        on_click=toggle_overlay,
        content=ft.SafeArea(
            content=ft.Column(
                [
                    # A. 顶部自定义 AppBar
                    ft.Container(
                        bgcolor=config.COLOR_BG_TRANSPARENT,  # 半透明黑色
                        padding=ft.Padding.only(top=30, left=15, right=15, bottom=10),
                        content=ft.Row(
                            [
                                # 返回按钮
                                back_button,
                                # 信息列
                                ft.Column(
                                    [
                                        ft.Text(
                                            topic.name,
                                            color=config.COLOR_TEXT_WHITE,
                                            size=config.TEXT_SIZE_MEDIUM,
                                            weight=ft.FontWeight.BOLD
                                        ),
                                        title_text
                                    ],
                                    spacing=2
                                ),
                                # 占位器
                                ft.Container(expand=True)
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                        )
                    ),
                    # 占位器
                    ft.Container(expand=True),
                    # B. 底部控制栏
                    ft.Container(
                        padding=20,
                        content=controls_row
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                expand=True
            )
        )
    )
    
    # --- Layer 2: 手势检测层 (Middle) ---
    gesture_detector = ft.GestureDetector(
        left=0,
        top=0,
        right=0,
        bottom=0,
        on_tap=None,  # 稍后绑定
        on_double_tap=None  # 稍后绑定
    )
    
    # --- Layer 1: 视频层 (Bottom) ---
    # 视频层容器将在初始化时设置
    
    # --- 创建 Stack ---
    stack_layers = ft.Stack(
        expand=True,
        controls=[
            # Layer 1: 视频层 (Bottom)
            video_container,
            # Layer 2: 手势检测层 (Middle)
            gesture_detector,
            # Layer 3: UI 覆盖层 (Top)
            overlay_container
        ]
    )

    # --- 绑定事件处理函数 ---
    
    # 绑定手势事件
    gesture_detector.on_tap = toggle_overlay
    gesture_detector.on_double_tap = toggle_play_pause
    
    # 绑定返回按钮事件
    back_button.on_click = on_back_nav_click
    
    # --- Initialization ---
    
    if total_questions > 0:
        first_q = questions[0]
        # 初始加载第一个视频
        if 0 in first_q.videos:
            init_src = utils.get_video_src(first_q.videos[0])
            # 直接创建初始 Video
            video_container.content = ftv.Video(
                expand=True,
                autoplay=True,
                show_controls=False,
                playlist=[ftv.VideoMedia(init_src)],
                fit=ft.BoxFit.CONTAIN,
                filter_quality=ft.FilterQuality.MEDIUM
            )
        
        controls_row.controls = [btn_repeat, btn_forget, btn_correct]

    return ft.View(
        route=f"/play/{topic.id}",
        padding=0,
        controls=[stack_layers]
    )
