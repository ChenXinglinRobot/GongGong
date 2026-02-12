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


def get_player_view(page: ft.Page, topic: Topic):
    """核心播放页面 - 使用 Stack 三层架构实现沉浸式覆盖"""
    current_q_index = 0
    questions: List[Question] = topic.questions
    total_questions = len(questions)

    # --- UI Controls Definition ---
    
    # 按钮定义
    btn_repeat = ft.FilledButton(
        content=ft.Text("听不清 / 再说一遍"),
        icon=ft.Icons.HEARING,
        style=ft.ButtonStyle(bgcolor=config.COLOR_BTN_REPEAT),
        height=config.BTN_HEIGHT,
        expand=True
    )
    
    btn_forget = ft.FilledButton(
        content=ft.Text("忘记了"),
        icon=ft.Icons.HELP_OUTLINE,
        style=ft.ButtonStyle(bgcolor=config.COLOR_BTN_FORGET),
        height=config.BTN_HEIGHT,
        expand=True
    )

    btn_correct = ft.FilledButton(
        content=ft.Text("回答正确"),
        icon=ft.Icons.CHECK_CIRCLE,
        style=ft.ButtonStyle(bgcolor=config.COLOR_BTN_CORRECT),
        height=config.BTN_HEIGHT,
        expand=True
    )

    btn_next = ft.FilledButton(
        content=ft.Text("下一题"),
        icon=ft.Icons.ARROW_FORWARD,
        style=ft.ButtonStyle(bgcolor=config.COLOR_BTN_NEXT),
        height=config.BTN_HEIGHT,
        expand=True
    )
    
    btn_finish = ft.FilledButton(
        content=ft.Text("完成 - 返回菜单"),
        icon=ft.Icons.HOME,
        style=ft.ButtonStyle(bgcolor=config.COLOR_BTN_FINISH),
        height=config.BTN_HEIGHT,
        expand=True
    )

    btn_retry = ft.FilledButton(
        content=ft.Text("重试本题"),
        icon=ft.Icons.REFRESH,
        style=ft.ButtonStyle(bgcolor=config.COLOR_BTN_RETRY),
        height=config.BTN_HEIGHT,
        expand=True
    )

    btn_skip = ft.FilledButton(
        content=ft.Text("跳过"),
        icon=ft.Icons.SKIP_NEXT,
        style=ft.ButtonStyle(bgcolor=config.COLOR_BTN_SKIP),
        height=config.BTN_HEIGHT,
        expand=True
    )

    controls_row = ft.Row(
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER,
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
                        padding=ft.padding.only(top=30, left=15, right=15, bottom=10),
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

    # --- Logic ---

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
    
    # --- Handlers ---
    
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

    # Bind handlers
    btn_repeat.on_click = on_repeat_click
    btn_forget.on_click = on_forget_click
    btn_correct.on_click = on_correct_click
    btn_retry.on_click = on_retry_click
    btn_next.on_click = on_next_or_skip_click
    btn_skip.on_click = on_next_or_skip_click
    btn_finish.on_click = on_finish_click

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
