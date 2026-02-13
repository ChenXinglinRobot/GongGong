"""
简化版测试：验证 ft.Scale 的 alignment 参数

测试目的：
1. 确认 ft.Scale 支持 alignment 参数
2. 测试不同 alignment 值的效果
3. 为升级计划提供准确的技术信息
"""

import flet as ft


def main(page: ft.Page):
    """主函数：测试 Scale 的 alignment 参数"""
    page.title = "Scale Alignment 测试 v2"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.spacing = 30

    # 状态标记
    is_scaled = False
    
    # 测试结果记录
    test_results = []

    # 测试不同的 alignment 值
    test_cases = [
        ("CENTER", ft.Alignment.CENTER, ft.Colors.BLUE),
        ("TOP_LEFT", ft.Alignment.TOP_LEFT, ft.Colors.RED),
        ("TOP_RIGHT", ft.Alignment.TOP_RIGHT, ft.Colors.GREEN),
        ("BOTTOM_LEFT", ft.Alignment.BOTTOM_LEFT, ft.Colors.ORANGE),
        ("BOTTOM_RIGHT", ft.Alignment.BOTTOM_RIGHT, ft.Colors.PURPLE),
    ]

    boxes = []
    
    for name, alignment, color in test_cases:
        # 测试构造函数是否接受 alignment 参数
        try:
            scale_obj = ft.Scale(scale=1.0, alignment=alignment)
            supported = True
            test_results.append(f"ft.Scale(scale=1.0, alignment={name}): ✅ 支持")
        except TypeError as e:
            scale_obj = ft.Scale(scale=1.0)
            supported = False
            test_results.append(f"ft.Scale(scale=1.0, alignment={name}): ❌ 不支持 ({e})")
        
        box = ft.Container(
            width=80,
            height=80,
            bgcolor=color,
            border_radius=5,
            scale=scale_obj,
            animate_scale=ft.Animation(
                duration=600,
                curve=ft.AnimationCurve.EASE_OUT,
            ),
            content=ft.Text(name, color=ft.Colors.WHITE, size=10),
            alignment=ft.Alignment.CENTER,
            data={"name": name, "alignment": alignment, "supported": supported}
        )
        boxes.append(box)

    # 结果显示
    result_text = ft.Text(
        value="测试结果:\n" + "\n".join(test_results),
        size=12,
        color=ft.Colors.BLACK,
        selectable=True,
    )

    def toggle_scale(e):
        """切换缩放状态"""
        nonlocal is_scaled
        is_scaled = not is_scaled
        target = 2.0 if is_scaled else 1.0
        
        for box in boxes:
            if box.data["supported"]:
                box.scale = ft.Scale(scale=target, alignment=box.data["alignment"])
            else:
                box.scale = ft.Scale(scale=target)
        
        page.update()

    page.add(
        ft.Text("Scale Alignment 参数测试", size=16, weight=ft.FontWeight.BOLD),
        result_text,
        ft.Text("点击按钮观察不同对齐点的缩放效果：", size=14),
        ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            controls=boxes,
        ),
        ft.Button(
            f"切换缩放 (当前: {'1x' if not is_scaled else '2x'})",
            on_click=toggle_scale,
        ),
        ft.Text("观察要点：", size=12, color=ft.Colors.GREY),
        ft.Text("1. 每个方块是否从指定的对齐点缩放？", size=12, color=ft.Colors.GREY),
        ft.Text("2. BOTTOM_RIGHT 是否真的从右下角缩放？", size=12, color=ft.Colors.GREY),
        ft.Text("3. 缩放动画是否平滑？", size=12, color=ft.Colors.GREY),
    )


ft.run(main)
