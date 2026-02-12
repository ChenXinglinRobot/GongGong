import flet as ft
from typing import List, Callable, Awaitable
from data_loader import Topic
import config


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
                        ft.Text(f"包含 {len(topic.questions)} 个问题", size=12),
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
