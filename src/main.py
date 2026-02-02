import flet as ft
import flet_video as ftv


async def main(page: ft.Page):
    """
    主函数，构建应用界面并处理交互逻辑。
    """
    # 页面设置
    page.title = "怀旧疗法辅助应用"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0

    # 构建播放列表（路径相对于assets_dir="assets"）
    playlist = [
        ftv.VideoMedia("/question_1.mp4"),        # 索引0: 提问视频
        ftv.VideoMedia("/correct_reaction.mp4"),  # 索引1: 正确反馈视频
        ftv.VideoMedia("/guide_reaction.mp4")     # 索引2: 引导反馈视频
    ]

    # 创建视频控件
    video = ftv.Video(
        playlist=playlist,
        playlist_mode=ftv.PlaylistMode.NONE,
        aspect_ratio=16 / 9,
        autoplay=True,          # 初始化自动播放提问视频
        show_controls=False     # 隐藏控制条，防止误触
    )

    # 创建按钮
    # 场景1按钮：提问中
    btn_correct = ft.FilledButton(
        content=ft.Text("回答正确"),
        expand=True,            # 在Row中扩展以填充可用空间
        height=100,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        on_click=lambda e: page.run_task(handle_correct_click, e, video)
    )
    btn_forgot = ft.FilledButton(
        content=ft.Text("忘记了"),
        expand=True,
        height=100,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        on_click=lambda e: page.run_task(handle_forgot_click, e, video)
    )

    # 场景2按钮：播放正确反馈中
    btn_next = ft.FilledButton(
        content=ft.Text("下一题"),
        expand=True,
        height=100,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        on_click=lambda e: page.run_task(handle_next_click, e, video),
        visible=False  # 初始隐藏
    )

    # 场景3按钮：播放引导反馈中
    btn_retry = ft.FilledButton(
        content=ft.Text("重试"),
        expand=True,
        height=100,
        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=10)),
        on_click=lambda e: page.run_task(handle_retry_click, e, video),
        visible=False  # 初始隐藏
    )

    # 按钮容器（底部控制面板）
    button_row = ft.Row(
        controls=[btn_correct, btn_forgot, btn_next, btn_retry],
        alignment=ft.MainAxisAlignment.SPACE_EVENLY,
        expand=True
    )

    control_panel = ft.Container(
        content=button_row,
        bgcolor="#CFD8DC",  # BLUE_GREY_100 的十六进制颜色代码
        border_radius=ft.BorderRadius(20, 20, 20, 20),
        padding=20,
        expand=1  # 占据下半部分1/3高度
    )

    # 视频容器（上半部分）
    video_container = ft.Container(
        content=video,
        expand=2,  # 占据上半部分2/3高度
        alignment=ft.Alignment(0, 0)  # 居中
    )

    # 主布局：垂直排列，2:1分割
    main_column = ft.Column(
        controls=[video_container, control_panel],
        spacing=0,
        expand=True
    )

    # 使用SafeArea包裹，避免刘海和手势条遮挡
    safe_area = ft.SafeArea(
        content=main_column,
        expand=True
    )

    # 将控件添加到页面
    page.add(safe_area)

    # 存储按钮引用以便更新
    page.btn_correct = btn_correct
    page.btn_forgot = btn_forgot
    page.btn_next = btn_next
    page.btn_retry = btn_retry
    page.video = video

    # 初始状态：显示提问按钮
    update_button_visibility(page, show_question=True)


def update_button_visibility(page, show_question=False, show_correct=False, show_guide=False):
    """
    更新按钮可见性。

    参数:
        page: ft.Page 对象
        show_question: 是否显示提问场景按钮（回答正确、忘记了）
        show_correct: 是否显示正确反馈场景按钮（下一题）
        show_guide: 是否显示引导反馈场景按钮（重试）
    """
    page.btn_correct.visible = show_question
    page.btn_forgot.visible = show_question
    page.btn_next.visible = show_correct
    page.btn_retry.visible = show_guide
    page.update()


async def handle_correct_click(e, video):
    """
    处理“回答正确”按钮点击。
    跳转到正确反馈视频（索引1），并切换按钮状态。
    """
    await video.jump_to(1)
    # 获取当前页面
    page = e.page
    update_button_visibility(page, show_correct=True)


async def handle_forgot_click(e, video):
    """
    处理“忘记了”按钮点击。
    跳转到引导反馈视频（索引2），并切换按钮状态。
    """
    await video.jump_to(2)
    page = e.page
    update_button_visibility(page, show_guide=True)


async def handle_next_click(e, video):
    """
    处理“下一题”按钮点击。
    跳转回提问视频（索引0），并切换按钮状态。
    """
    await video.jump_to(0)
    page = e.page
    update_button_visibility(page, show_question=True)


async def handle_retry_click(e, video):
    """
    处理“重试”按钮点击。
    跳转回提问视频（索引0），并切换按钮状态。
    """
    await video.jump_to(0)
    page = e.page
    update_button_visibility(page, show_question=True)


# # 启动应用
# if __name__ == "__main__":
#     ft.run(main, assets_dir="assets")
if __name__ == "__main__":
    # 这一行会让程序不弹窗，而是自动打开你的默认浏览器（Chrome/Edge）
    ft.run(main, assets_dir="assets", view=ft.AppView.WEB_BROWSER)