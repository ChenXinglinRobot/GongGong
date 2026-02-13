"""
测试 ft.Scale 是否支持 alignment 参数（缩放中心点控制）

测试目的：
1. 验证 ft.Scale 构造函数是否接受 alignment 参数
2. 对比不同 alignment 下的缩放效果（中心 vs 左上角）
3. 如果不支持，程序会报错，这就是最直接的验证

运行方式：
  uv run flet run test_scale_alignment.py
"""

import flet as ft


def main(page: ft.Page):
    """主函数：测试 Scale 的 alignment 参数"""
    page.title = "Scale Alignment 测试"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.spacing = 30

    # 状态标记
    is_scaled = False

    # --- 测试1：默认缩放（应该从中心缩放） ---
    box1 = ft.Container(
        width=100,
        height=100,
        bgcolor=ft.Colors.BLUE,
        border_radius=5,
        scale=ft.Scale(scale=1.0),
        animate_scale=ft.Animation(
            duration=600,
            curve=ft.AnimationCurve.EASE_OUT,
        ),
        content=ft.Text("默认中心", color=ft.Colors.WHITE, size=12),
        alignment=ft.Alignment.CENTER,
    )

    # --- 测试2：尝试使用 alignment=TOP_LEFT 缩放 ---
    try:
        scale_with_alignment = ft.Scale(
            scale=1.0,
            alignment=ft.Alignment.TOP_LEFT,)
        test2_success = True
    except TypeError as e:
        scale_with_alignment = ft.Scale(scale=1.0)
        test2_success = False

    box2 = ft.Container(
        width=100,
        height=100,
        bgcolor=ft.Colors.RED,
        border_radius=5,
        scale=scale_with_alignment,
        animate_scale=ft.Animation(
            duration=600,
            curve=ft.AnimationCurve.EASE_OUT,
        ),
        content=ft.Text("左上角", color=ft.Colors.WHITE, size=12),
        alignment=ft.Alignment.CENTER,
    )

    # --- 测试3：尝试使用 scale_x / scale_y + alignment ---
    try:
        scale_xy_with_alignment = ft.Scale(
            scale_x=1.0,
            scale_y=1.0,
            alignment=ft.Alignment.BOTTOM_RIGHT,
        )
        test3_success = True
    except TypeError as e:
        scale_xy_with_alignment = ft.Scale(scale_x=1.0, scale_y=1.0)
        test3_success = False

    box3 = ft.Container(
        width=100,
        height=100,
        bgcolor=ft.Colors.GREEN,
        border_radius=5,
        scale=scale_xy_with_alignment,
        animate_scale=ft.Animation(
            duration=600,
            curve=ft.AnimationCurve.EASE_OUT,
        ),
        content=ft.Text("右下角", color=ft.Colors.WHITE, size=12),
        alignment=ft.Alignment.CENTER,
    )

    # --- 结果显示 ---
    result_text = ft.Text(
        value=(
            f"测试结果:\n"
            f"  ft.Scale(scale=1.0, alignment=TOP_LEFT): {'✅ 支持' if test2_success else '❌ 不支持'}\n"
            f"  ft.Scale(scale_x=1.0, scale_y=1.0, alignment=BOTTOM_RIGHT): {'✅ 支持' if test3_success else '❌ 不支持'}"
        ),
        size=14,
        color=ft.Colors.BLACK,
    )

    def toggle_scale(e):
        """切换缩放状态，观察不同 alignment 的缩放效果"""
        nonlocal is_scaled
        is_scaled = not is_scaled
        target = 2.0 if is_scaled else 1.0

        # 默认中心缩放
        box1.scale = ft.Scale(scale=target)

        # 左上角缩放（如果支持）
        if test2_success:
            box2.scale = ft.Scale(scale=target, alignment=ft.Alignment.TOP_LEFT)
        else:
            box2.scale = ft.Scale(scale=target)

        # 右下角缩放（如果支持）
        if test3_success:
            box3.scale = ft.Scale(scale_x=target, scale_y=target, alignment=ft.Alignment.BOTTOM_RIGHT)
        else:
            box3.scale = ft.Scale(scale_x=target, scale_y=target)

        page.update()

    page.add(
        result_text,
        ft.Text("点击按钮后观察三个方块的缩放中心点是否不同：", size=14),
        ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            controls=[
                ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[ft.Text("默认(中心)"), box1],
                ),
                ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[ft.Text("TOP_LEFT"), box2],
                ),
                ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[ft.Text("BOTTOM_RIGHT"), box3],
                ),
            ],
        ),
        ft.Button(
            "切换缩放 (1x ↔ 2x)",
            on_click=toggle_scale,
        ),
    )


ft.run(main)
