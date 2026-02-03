import flet as ft
import flet_video as ftv
from typing import List, Callable, Awaitable
from data_loader import Topic, Question

# ==========================================
# 1. 辅助函数 (Android/Web 专用 - 保持相对路径)
# ==========================================

def _get_video_src(raw_path: str) -> str:
    """
    [Android/Web 专用]
    直接返回相对路径，不要转换为绝对路径。
    例如: "assets/topic/video.mp4" -> "/topic/video.mp4"
    """
    clean_path = raw_path.replace("\\", "/")
    if clean_path.startswith("assets/"):
        return "/" + clean_path.split("/", 1)[1]
    return "/" + clean_path if not clean_path.startswith("/") else clean_path

# ==========================================
# 2. 菜单视图 (Menu View)
# ==========================================

def get_menu_view(page: ft.Page, topics: List[Topic], on_topic_click: Callable[[Topic], Awaitable[None]]):
    """主菜单：展示所有可用的话题"""
    topic_buttons = []

    def create_click_handler(t: Topic):
        async def handler(e):
            await on_topic_click(t)
        return handler

    for topic in topics:
        btn = ft.Container(
            content=ft.FilledButton(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.VIDEO_LIBRARY, size=40),
                        ft.Text(topic.name, size=20, weight=ft.FontWeight.BOLD),
                        ft.Text(f"包含 {len(topic.questions)} 个环节", size=12),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                style=ft.ButtonStyle(
                    shape=ft.RoundedRectangleBorder(radius=10),
                    padding=20,
                ),
                on_click=create_click_handler(topic),
                height=160,
            ),
            padding=10,
        )
        topic_buttons.append(btn)

    menu_grid = ft.GridView(
        expand=True,
        runs_count=3,
        max_extent=300,
        child_aspect_ratio=1.0,
        spacing=10,
        run_spacing=10,
        controls=topic_buttons,
    )

    return ft.View(
        route="/",
        controls=[
            ft.SafeArea(
                content=ft.Column(
                    [
                        ft.Container(
                            content=ft.Text("请选择一个回忆话题", size=32, weight=ft.FontWeight.BOLD),
                            padding=ft.padding.only(left=10, top=20, bottom=10)
                        ),
                        ft.Divider(),
                        menu_grid,
                    ],
                    expand=True,
                ),
                expand=True
            )
        ],
    )

# ==========================================
# 3. 播放器视图 (Player View - Core Logic)
# ==========================================

def get_player_view(page: ft.Page, topic: Topic):
    """核心播放页面"""
    current_q_index = 0
    questions: List[Question] = topic.questions
    total_questions = len(questions)

    # --- UI Controls Definition ---
    
    # [关键修改] 定义一个容器，而不是直接定义 Video
    # 稍后我们将把 Video 组件动态塞入这个容器
    video_container = ft.Container(
        expand=2, 
        bgcolor=ft.Colors.BLACK,
        alignment=ft.Alignment(0, 0),
        content=ft.ProgressRing() # 初始显示加载圈
    )

    # 按钮定义
    btn_repeat = ft.FilledButton(
        content=ft.Text("听不清 / 再说一遍"),
        icon=ft.Icons.HEARING,
        style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_400),
        height=60,
        expand=True
    )
    
    btn_forget = ft.FilledButton(
        content=ft.Text("忘记了"),
        icon=ft.Icons.HELP_OUTLINE,
        style=ft.ButtonStyle(bgcolor=ft.Colors.ORANGE_400),
        height=60,
        expand=True
    )

    btn_correct = ft.FilledButton(
        content=ft.Text("回答正确"),
        icon=ft.Icons.CHECK_CIRCLE,
        style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_500),
        height=60,
        expand=True
    )

    btn_next = ft.FilledButton(
        content=ft.Text("下一题"),
        icon=ft.Icons.ARROW_FORWARD,
        style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_700),
        height=60,
        expand=True
    )
    
    btn_finish = ft.FilledButton(
        content=ft.Text("完成 - 返回菜单"),
        icon=ft.Icons.HOME,
        style=ft.ButtonStyle(bgcolor=ft.Colors.PURPLE_500),
        height=60,
        expand=True
    )

    btn_retry = ft.FilledButton(
        content=ft.Text("重试本题"),
        icon=ft.Icons.REFRESH,
        style=ft.ButtonStyle(bgcolor=ft.Colors.BLUE_GREY_500),
        height=60,
        expand=True
    )

    btn_skip = ft.FilledButton(
        content=ft.Text("跳过"),
        icon=ft.Icons.SKIP_NEXT,
        style=ft.ButtonStyle(bgcolor=ft.Colors.RED_300),
        height=60,
        expand=True
    )

    controls_row = ft.Row(
        spacing=20,
        alignment=ft.MainAxisAlignment.CENTER,
    )

    title_text = ft.Text(f"当前进度: 1 / {total_questions}", size=18)

    # --- Logic ---

    async def update_ui_state(state_id: int):
        nonlocal current_q_index
        if current_q_index >= total_questions:
            return

        q = questions[current_q_index]
        raw_path = q.videos.get(state_id)
        
        if raw_path:
            src = _get_video_src(raw_path)
            print(f"Switching video to: {src}") 
            
            # [关键修复] 暴力重绘策略
            # 不更新旧 Video，而是创建一个全新的 Video 组件
            # 这样能强制浏览器/Android 重新加载资源
            new_player = ftv.Video(
                expand=True,
                autoplay=True,      # 新组件创建即播放
                show_controls=False,
                playlist=[ftv.VideoMedia(src)],
                aspect_ratio=16/9,
                filter_quality=ft.FilterQuality.HIGH,
                # 即使是新组件，最好也加个 key 确保唯一性 (可选，但推荐)
                key=f"video_{q.id}_{state_id}_{current_q_index}"
            )
            
            # 将容器内容替换为新播放器
            video_container.content = new_player
            # 注意：新组件不需要 await video.play()，因为有 autoplay=True
        else:
            print(f"Error: Missing video for State {state_id} in Question {q.id}")
            video_container.content = ft.Text("视频缺失", color=ft.Colors.RED)

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

    # --- Initialization ---
    
    if total_questions > 0:
        first_q = questions[0]
        # 初始加载第一个视频
        if 0 in first_q.videos:
            init_src = _get_video_src(first_q.videos[0])
            # 直接创建初始 Video
            video_container.content = ftv.Video(
                expand=True,
                autoplay=True,
                show_controls=False,
                playlist=[ftv.VideoMedia(init_src)],
                aspect_ratio=16/9,
                filter_quality=ft.FilterQuality.HIGH
            )
        
        controls_row.controls = [btn_repeat, btn_forget, btn_correct]

    return ft.View(
        route=f"/play/{topic.id}",
        padding=0,
        controls=[
            ft.SafeArea(
                content=ft.Column(
                    [
                        ft.Container(
                            content=ft.Row(
                                [
                                    ft.IconButton(ft.Icons.ARROW_BACK, on_click=on_back_nav_click),
                                    ft.Text(f"正在进行: {topic.name}", size=20, weight=ft.FontWeight.BOLD),
                                    ft.Container(expand=True),
                                    title_text
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                            ),
                            padding=10
                        ),
                        # [Critical] 这里放置的是 video_container，不是 video_player
                        video_container,
                        ft.Container(
                            content=controls_row,
                            expand=1,
                            padding=20,
                            bgcolor=ft.Colors.GREY_100,
                            alignment=ft.Alignment(0, 0)
                        )
                    ],
                    expand=True,
                    spacing=0
                ),
                expand=True
            )
        ]
    )