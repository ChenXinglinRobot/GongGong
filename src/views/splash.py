import flet as ft
import asyncio

def get_splash_view(page: ft.Page):
    """
    创建静态的开屏视图（初始透明状态）
    
    参数:
        page: ft.Page - Flet页面对象
    
    返回:
        tuple: (视图对象, 图像组件, None) - 返回None作为文本组件占位符
    """
    # 创建图像组件
    image = ft.Image(
        src="assets/splash_anim_fixed.gif",
        opacity=0,  # 初始透明
        animate_opacity=2000,  # 2秒淡入动画
        fit=ft.BoxFit.CONTAIN,
    )
    
    # 创建全屏容器，直接包含图像
    container = ft.Container(
        content=image,
        expand=True,
        bgcolor="#F6F1DE",  # 与GIF边缘一致
        alignment=ft.Alignment.CENTER,  # 居中显示，确保图片在屏幕内完全可见
    )
    
    # 返回视图和组件引用（文本组件返回None）
    return ft.View(
        route="/splash",
        controls=[container],
        padding=0,
    ), image, None

async def start_splash_animation(page: ft.Page, image: ft.Image, text: ft.Text):
    """
    启动开屏动画
    
    参数:
        page: ft.Page - Flet页面对象
        image: ft.Image - 图像组件
        text: ft.Text - 文本组件（已弃用，保留参数以保持API兼容性）
    """
    # 等待确保视图已渲染
    await asyncio.sleep(0.1)
    
    # 触发淡入动画（只处理图像，文字已移除）
    image.opacity = 1
    page.update()
    
    # 等待动画完成（2秒淡入 + 2秒展示）
    await asyncio.sleep(4)
    
    # 跳转到根路由（welcome视图）
    await page.push_route("/")
