# V5.0 FINAL FIX
import flet as ft
import data_loader
import views

async def main(page: ft.Page):
    # 1. 初始化设置
    page.title = "阿尔兹海默症回忆疗法"
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # 2. 加载数据
    topics = data_loader.load_topics("assets")
    topic_map = {t.id: t for t in topics}

    # 3. 路由变换逻辑
    async def route_change(e):
        page.views.clear()
        
        # 技巧：如果是手动调用，e 可能是 page 对象
        # page 对象和 event 对象都有 route 属性，所以这里都能由
        try:
            current_route = e.route
        except AttributeError:
            current_route = page.route
            
        # 路由 1: 首页菜单
        if current_route == "/":
            async def on_topic_select(topic):
                await page.push_route(f"/play/{topic.id}")
            
            page.views.append(
                views.get_menu_view(page, topics, on_topic_select)
            )

        # 路由 2: 播放页
        elif current_route.startswith("/play/"):
            topic_id = current_route.split("/")[-1]
            selected_topic = topic_map.get(topic_id)
            
            if selected_topic:
                page.views.append(
                    views.get_player_view(page, selected_topic)
                )
            else:
                await page.push_route("/")

        page.update()

    async def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        await page.push_route(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    # [关键修复] 手动触发一次路由逻辑，解决白屏问题
    # 这里传入 page 替代 event，避免构造 RouteChangeEvent 的报错
    await route_change(page)

if __name__ == "__main__":
    ft.run(main, assets_dir="assets")

# #     ft.run(main, assets_dir="assets")
# if __name__ == "__main__":
#     # 这一行会让程序不弹窗，而是自动打开你的默认浏览器（Chrome/Edge）
#     ft.run(main, assets_dir="assets", view=ft.AppView.WEB_BROWSER)