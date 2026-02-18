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
    
    # 设置全屏模式（Android上会隐藏顶部状态栏）
    page.window_full_screen = True

    # ==========================================
    # 🔥 Flet 0.80.5 修复：移除所有 overlay.append()
    # FilePicker 和 PermissionHandler 现在都是 Service 类型
    # 使用内联实例化模式，不再需要挂载到 overlay
    # ==========================================
    
    # 注意：不再需要创建全局的 FilePicker 或 PermissionHandler
    # 它们将在需要时直接实例化使用
    
    # ==========================================
    # 🔥 Flet 0.80.5 修复：Audio 是 Service，注册到 page.services
    # 根据 Flet 作者 (FeodorFitsner) 的官方指导：
    # "Audio is a service and should not be added to a page with visible controls.
    #  Add it to page.services to retain the reference to it."
    # ==========================================
    from audio_manager import AudioManager
    
    # 初始化音频管理器
    audio_manager = AudioManager(page)
    
    # 将所有音频实例注册到 page.services
    all_audios = audio_manager.get_controls()
    page.services.extend(all_audios)
    page.update()
    
    # 通过 page.data 共享给各个 view
    page.data = page.data or {}
    page.data["audio_manager"] = audio_manager

    # ==========================================
    # 2. 读取配置 (使用 ft.SharedPreferences())
    # ==========================================
    stored_path = None
    try:
        # 使用 ft.SharedPreferences() 实例来访问存储
        shared_prefs = ft.SharedPreferences()
        if await shared_prefs.contains_key("video_root_path"):
            stored_path = await shared_prefs.get("video_root_path")
    except Exception as e:
        print(f"读取配置出错 (可忽略): {e}")
        stored_path = None
    
    topics = []
    topic_map = {}
    if stored_path and Path(stored_path).exists():
        topics = data_loader.load_topics(stored_path)
        topic_map = {t.id: t for t in topics}
    
    # 3. 路由变换逻辑 - 修复 Android 返回键导航问题
    async def route_change(e):
        try:
            current_route = e.route
        except AttributeError:
            current_route = page.route
        
        # 🎵 BGM 控制逻辑
        if current_route.startswith("/play/"):
            # 进入播放器页面时停止 BGM
            if audio_manager:
                await audio_manager.stop_bgm()
                print("进入播放器页面，停止背景音乐")
        elif current_route == "/setup":
            # 进入设置页面时停止 BGM
            if audio_manager:
                await audio_manager.stop_bgm()
                print("进入设置页面，停止背景音乐")
        # 进入欢迎页面（/）时 BGM 会自动在 welcome.py 中播放
        # 进入开屏页面（/splash）时不需要处理 BGM
        
        # 路由分发 - 采用栈式导航策略
        # 1. 如果是根路由（/splash, /, /setup），清空栈并添加新页面
        # 2. 如果是子路由（/play/...），添加到栈顶
        if current_route == "/splash":
            # 清空视图栈，只保留开屏页面
            page.views.clear()
            # 获取splash视图和组件引用
            splash_view, image, text = views.get_splash_view(page)
            page.views.append(splash_view)
            page.update()
            
            # 启动动画任务
            asyncio.create_task(views.start_splash_animation(page, image, text))
            
        elif current_route == "/":
            # 清空视图栈，只保留欢迎页面
            page.views.clear()
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
                # 检查是否已经在播放器页面（避免重复添加）
                if len(page.views) == 0 or not page.views[-1].route.startswith("/play/"):
                    page.views.append(views.get_player_view(page, selected_topic))
            else:
                await page.push_route("/")
        
        elif current_route == "/setup":
            # 清空视图栈，只保留设置页面
            page.views.clear()
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
        """处理 Android 返回键和页面弹出"""
        if len(page.views) > 1:
            # 弹出栈顶页面
            page.views.pop()
            # 获取新的栈顶页面
            top_view = page.views[-1]
            # 更新路由到新栈顶页面的路由
            page.route = top_view.route
            page.update()
        else:
            # 如果栈中只有一个页面，应用退出（Android 默认行为）
            # 这里可以添加确认退出的逻辑，但为了简单起见，我们让应用退出
            pass

    # 4. 应用生命周期监听 - 修复后台音频播放问题
    async def on_app_lifecycle_state_change(e):
        """处理应用生命周期状态变化"""
        print(f"应用生命周期状态变化: {e.state}")
        
        if e.state in [ft.AppLifecycleState.HIDE, ft.AppLifecycleState.PAUSE]:
            # 应用进入后台，释放所有音频资源
            if audio_manager:
                await audio_manager.release_all()
                print("应用进入后台，释放所有音频资源")
        elif e.state == ft.AppLifecycleState.RESUME:
            # 应用回到前台，根据当前路由恢复音频
            if audio_manager and page.route == "/":
                # 如果在欢迎页面，恢复播放 BGM
                await audio_manager.play_bgm()
                print("应用回到前台，恢复背景音乐")
    
    page.on_app_lifecycle_state_change = on_app_lifecycle_state_change
    
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    # 设置初始路由为/splash
    await page.push_route("/splash")

if __name__ == "__main__":
    ft.run(main)
    # ft.app(target=main, view=ft.AppView.WEB_BROWSER)
