import flet as ft
from typing import Callable, Awaitable
from pathlib import Path
import config

# ==========================================
# 设置向导视图 (Setup View) - Flet 0.80.5 修复版
# ==========================================

def get_setup_view(
    page: ft.Page, 
    on_success: Callable[[str], Awaitable[None]]
):
    """设置向导页面 - 使用 Flet 0.80.5 内联实例化 API"""
    
    # 1. 准备变量 (如果是移动端)
    is_mobile = page.platform in [ft.PagePlatform.ANDROID, ft.PagePlatform.IOS]

    # UI 组件
    status_text = ft.Text("请选择手机内的'GongGong'视频文件夹", size=config.TEXT_SIZE_LARGE, text_align=ft.TextAlign.CENTER)
    selected_path_text = ft.Text("", size=14, color=config.COLOR_TEXT_GREY, text_align=ft.TextAlign.CENTER)
    select_button = ft.FilledButton(
        content=ft.Row(
            [ft.Icon(ft.Icons.FOLDER_OPEN), ft.Text("授权并选择文件夹", size=config.TEXT_SIZE_MEDIUM)],
            alignment=ft.MainAxisAlignment.CENTER, spacing=10
        ),
        height=config.BTN_HEIGHT, width=300,
    )
    loading_ring = ft.ProgressRing(visible=False)
    error_text = ft.Text("", color=config.COLOR_TEXT_ERROR, text_align=ft.TextAlign.CENTER)
    
    async def handle_select_folder(e):
        select_button.disabled = True
        loading_ring.visible = True
        error_text.value = ""
        page.update()
        
        try:
            # 🔥 Flet 0.80.5 修复：内联实例化 PermissionHandler
            if is_mobile:
                try:
                    import flet_permission_handler as fph
                    # 直接实例化使用，不需要添加到 overlay
                    ph = fph.PermissionHandler()
                    status = await ph.request(fph.Permission.MANAGE_EXTERNAL_STORAGE)
                    if status != fph.PermissionStatus.GRANTED:
                        error_text.value = "存储权限被拒绝"
                        select_button.disabled = False
                        loading_ring.visible = False
                        page.update()
                        return
                except ImportError:
                    error_text.value = "权限处理器未安装"
                    select_button.disabled = False
                    loading_ring.visible = False
                    page.update()
                    return

            # 🔥 Flet 0.80.5 修复：内联实例化 FilePicker
            # 根据文档，FilePicker 现在可以直接实例化使用
            selected_path = await ft.FilePicker().get_directory_path(dialog_title="选择视频文件夹")
            
            if not selected_path:
                error_text.value = "已取消"
                select_button.disabled = False
                loading_ring.visible = False
                page.update()
                return

            # 验证文件夹内容
            path_obj = Path(selected_path)
            has_mp4_files = any(path_obj.glob("**/*.mp4"))
            has_topic_folders = any(d.name.startswith("topic_") and d.is_dir() for d in path_obj.iterdir())
            
            if not (has_mp4_files or has_topic_folders):
                error_text.value = "文件夹无效（未找到视频）"
                select_button.disabled = False
                loading_ring.visible = False
                page.update()
                return

            # 保存路径到共享首选项
            await page.shared_preferences.set("video_root_path", selected_path)
            selected_path_text.value = f"已选择: {selected_path}"
            await on_success(selected_path)

        except Exception as ex:
            error_text.value = f"错误: {str(ex)}"
            select_button.disabled = False
            loading_ring.visible = False
            page.update()
    
    select_button.on_click = handle_select_folder
    
    return ft.View(
        route="/setup",
        controls=[
            ft.SafeArea(
                content=ft.Column(
                    [
                        ft.Container(height=50),
                        ft.Icon(ft.Icons.VIDEO_SETTINGS, size=config.ICON_SIZE_LARGE, color=config.COLOR_ICON_BLUE),
                        status_text,
                        ft.Container(height=10),
                        selected_path_text,
                        ft.Container(height=30),
                        select_button,
                        ft.Container(height=20),
                        loading_ring,
                        error_text,
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    expand=True
                ),
                expand=True
            )
        ]
    )
