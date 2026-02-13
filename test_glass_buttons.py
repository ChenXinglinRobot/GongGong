"""
测试毛玻璃按钮效果
"""
import flet as ft
import sys
import os

# 将 src 目录添加到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

def create_glass_button(text, icon, color, on_click_handler, expand=True):
    """创建具有毛玻璃效果和完整交互反馈的按钮
    
    参数:
        text: 按钮文字
        icon: 图标名称
        color: 基础颜色（如 ft.Colors.BLUE_400）
        on_click_handler: 点击事件处理函数
        expand: 是否扩展填充可用空间
    """
    # 创建按钮容器
    btn_container = ft.Container(
        content=ft.Row(
            [
                ft.Icon(icon, color=ft.Colors.WHITE),
                ft.Text(text, color=ft.Colors.WHITE, size=16)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=10,
        ),
        padding=ft.Padding.symmetric(horizontal=20, vertical=15),
        border_radius=10,
        bgcolor=color + "40",  # 25%透明度
        blur=ft.Blur(10, 10, ft.BlurTileMode.CLAMP),
        border=ft.Border.all(1, ft.Colors.WHITE_24),
        animate=ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
        on_click=on_click_handler,
    )
    
    if expand:
        btn_container.expand = True
    
    # 交互状态变量
    btn_container.normal_color = color + "40"    # 25%透明度
    btn_container.hover_color = color + "60"     # 37.5%透明度
    btn_container.pressed_color = color + "80"   # 50%透明度
    
    # 交互事件处理
    def on_hover(e):
        if not getattr(btn_container, '_is_pressed', False):
            btn_container.bgcolor = btn_container.hover_color if e.data == "true" else btn_container.normal_color
            btn_container.update()
    
    def on_tap_down(e):
        btn_container._is_pressed = True
        btn_container.bgcolor = btn_container.pressed_color
        btn_container.update()
    
    def on_tap_up(e):
        btn_container._is_pressed = False
        btn_container.bgcolor = btn_container.hover_color if getattr(btn_container, '_is_hovering', False) else btn_container.normal_color
        btn_container.update()
    
    # 绑定事件
    btn_container.on_hover = on_hover
    btn_container.on_tap_down = on_tap_down
    btn_container.on_tap_up = on_tap_up
    
    # 跟踪悬停状态
    def update_hover_state(e):
        btn_container._is_hovering = e.data == "true"
    
    btn_container.on_hover = lambda e: (on_hover(e), update_hover_state(e))
    
    return btn_container

def main(page: ft.Page):
    page.title = "毛玻璃按钮效果测试"
    page.bgcolor = ft.Colors.BLACK
    
    # 创建背景图片（模拟视频背景）
    bg_image = ft.Image(
        src="https://picsum.photos/800/600?random=1",
        fit=ft.BoxFit.COVER,
        opacity=0.8,
    )
    
    # 创建背景模糊层
    bg_blur = ft.Container(
        expand=True,
        bgcolor=ft.Colors.BLACK_12,
        blur=ft.Blur(5, 5, ft.BlurTileMode.CLAMP),
    )
    
    # 创建按钮
    def on_button_click(e):
        print(f"按钮被点击: {e.control.content.controls[1].value}")
    
    btn_repeat = create_glass_button(
        "听不清 / 再说一遍",
        ft.Icons.HEARING,
        ft.Colors.BLUE_400,
        on_button_click,
        expand=True
    )
    
    btn_forget = create_glass_button(
        "忘记了",
        ft.Icons.HELP_OUTLINE,
        ft.Colors.ORANGE_400,
        on_button_click,
        expand=True
    )

    btn_correct = create_glass_button(
        "回答正确",
        ft.Icons.CHECK_CIRCLE,
        ft.Colors.GREEN_500,
        on_button_click,
        expand=True
    )

    btn_next = create_glass_button(
        "下一题",
        ft.Icons.ARROW_FORWARD,
        ft.Colors.GREEN_700,
        on_button_click,
        expand=True
    )
    
    btn_finish = create_glass_button(
        "完成 - 返回菜单",
        ft.Icons.HOME,
        ft.Colors.PURPLE_500,
        on_button_click,
        expand=True
    )

    btn_retry = create_glass_button(
        "重试本题",
        ft.Icons.REFRESH,
        ft.Colors.BLUE_GREY_500,
        on_button_click,
        expand=True
    )

    btn_skip = create_glass_button(
        "跳过",
        ft.Icons.SKIP_NEXT,
        ft.Colors.RED_300,
        on_button_click,
        expand=True
    )
    
    # 创建按钮行
    controls_row1 = ft.Row(
        [btn_repeat, btn_forget, btn_correct],
        spacing=15,
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )
    
    controls_row2 = ft.Row(
        [btn_next, btn_finish],
        spacing=15,
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )
    
    controls_row3 = ft.Row(
        [btn_retry, btn_skip],
        spacing=15,
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )
    
    # 创建说明文本
    instructions = ft.Column(
        [
            ft.Text("毛玻璃按钮效果测试", size=24, color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
            ft.Text("按钮具有以下特性：", size=16, color=ft.Colors.WHITE_70),
            ft.Text("1. 半透明背景（25%透明度）", size=14, color=ft.Colors.WHITE_70),
            ft.Text("2. 10px模糊效果", size=14, color=ft.Colors.WHITE_70),
            ft.Text("3. 白色边框增强可见性", size=14, color=ft.Colors.WHITE_70),
            ft.Text("4. 悬停时透明度增加（37.5%）", size=14, color=ft.Colors.WHITE_70),
            ft.Text("5. 按下时透明度进一步增加（50%）", size=14, color=ft.Colors.WHITE_70),
            ft.Container(height=20),
            ft.Text("请将鼠标悬停在按钮上并点击测试交互效果", size=16, color=ft.Colors.WHITE_70),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    
    # 创建主布局
    main_content = ft.Column(
        [
            ft.Container(height=50),
            instructions,
            ft.Container(height=40),
            controls_row1,
            ft.Container(height=20),
            controls_row2,
            ft.Container(height=20),
            controls_row3,
            ft.Container(expand=True),
        ],
        alignment=ft.MainAxisAlignment.START,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True,
    )
    
    # 创建堆叠布局
    stack = ft.Stack(
        [
            bg_image,
            bg_blur,
            ft.Container(
                content=main_content,
                alignment=ft.Alignment(0, 0),
                expand=True,
            )
        ],
        expand=True,
    )
    
    page.add(stack)

if __name__ == "__main__":
    ft.run(main)