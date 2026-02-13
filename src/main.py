# main.py
import flet as ft
import asyncio
from pathlib import Path
import data_loader
import views

async def main(page: ft.Page):
    # 1. 初始化设置
    page.title = "阿尔兹海默症回忆疗法"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.bgcolor = ft.Colors.BLACK

    # ==========================================
    # 🔥 Flet 0.80.5 修复：移除所有 overlay.append()
    # FilePicker 和 PermissionHandler 现在都是 Service 类型
    # 使用内联实例化模式，不再需要挂载到 overlay
    # ==========================================
    
    # 注意：不再需要创建全局的 FilePicker 或 PermissionHandler
    # 它们将在需要时直接实例化使用
    
    page.update()

    # ==========================================
    # 2. 读取配置 (回退到 page.shared_preferences)
    # ==========================================
    # 注意：控制台可能会出现 DeprecationWarning，请忽略它，这是正常的！
    stored_path = None
    try:
        if await page.shared_preferences.contains_key("video_root_path"):
            stored_path = await page.shared_preferences.get("video_root_path")
    except Exception as e:
        print(f"读取配置出错 (可忽略): {e}")
        stored_path = None
    
    topics = []
    topic_map = {}
    if stored_path and Path(stored_path).exists():
        topics = data_loader.load_topics(stored_path)
        topic_map = {t.id: t for t in topics}
    
    # 3. 路由变换逻辑
    async def route_change(e):
        # 🔥 步骤 A: 只清理视图，保留全局 overlay 组件
        page.views.clear()
        
        # 路由分发
        try:
            current_route = e.route
        except AttributeError:
            current_route = page.route
            
        if current_route == "/":
            if topics:
                # 定义 on_topic_enter 回调函数，当用户最终确认时，跳转到 /play/{topic.id}
                async def on_topic_enter(topic):
                    await page.push_route(f"/play/{topic.id}")
                # 使用新的 get_welcome_view 替换原来的 get_menu_view
                page.views.append(views.get_welcome_view(page, topics, on_topic_enter))
            else:
                await page.push_route("/setup")
        
        elif current_route.startswith("/play/"):
            if not topics:
                await page.push_route("/setup")
                return
            topic_id = current_route.split("/")[-1]
            selected_topic = topic_map.get(topic_id)
            if selected_topic:
                page.views.append(views.get_player_view(page, selected_topic))
            else:
                await page.push_route("/")
        
        elif current_route == "/setup":
            async def on_setup_success(selected_path: str):
                nonlocal topics, topic_map
                topics = data_loader.load_topics(selected_path)
                topic_map = {t.id: t for t in topics}
                if topics:
                    await page.push_route("/")
                else:
                    await page.push_route("/setup")
            
            # 🔥 Flet 0.80.5 修复：不再传递 file_picker 和 permission_handler
            # 这些组件现在在 views.py 中直接实例化使用
            page.views.append(
                views.get_setup_view(
                    page, 
                    on_setup_success
                )
            )

        page.update()

    async def view_pop(e):
        if len(page.views) > 1:
            page.views.pop()
            top_view = page.views[-1]
            await page.push_route(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    await route_change(page)

if __name__ == "__main__":
    ft.run(main)
    # ft.app(target=main, view=ft.AppView.WEB_BROWSER)
