"""
详细测试 ft.Scale 的参数兼容性

测试目的：
1. 验证 scale 与 scale_x/scale_y 的区别
2. 测试 alignment 与不同参数组合的兼容性
3. 找出绿色方块不动的原因
"""

import flet as ft


def main(page: ft.Page):
    """主函数：详细测试 Scale 参数"""
    page.title = "Scale 参数详细测试"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.spacing = 20

    is_scaled = False
    test_log = []

    # 测试不同的参数组合
    test_cases = [
        # (描述, 参数, 颜色)
        ("scale=1.0", {"scale": 1.0}, ft.Colors.BLUE),
        ("scale=1.0, alignment=CENTER", {"scale": 1.0, "alignment": ft.Alignment.CENTER}, ft.Colors.BLUE_300),
        ("scale=1.0, alignment=TOP_LEFT", {"scale": 1.0, "alignment": ft.Alignment.TOP_LEFT}, ft.Colors.RED),
        ("scale=1.0, alignment=BOTTOM_RIGHT", {"scale": 1.0, "alignment": ft.Alignment.BOTTOM_RIGHT}, ft.Colors.RED_300),
        ("scale_x=1.0, scale_y=1.0", {"scale_x": 1.0, "scale_y": 1.0}, ft.Colors.GREEN),
        ("scale_x=1.0, scale_y=1.0, alignment=CENTER", {"scale_x": 1.0, "scale_y": 1.0, "alignment": ft.Alignment.CENTER}, ft.Colors.GREEN_300),
        ("scale_x=1.0, scale_y=1.0, alignment=TOP_LEFT", {"scale_x": 1.0, "scale_y": 1.0, "alignment": ft.Alignment.TOP_LEFT}, ft.Colors.ORANGE),
        ("scale_x=1.0, scale_y=1.0, alignment=BOTTOM_RIGHT", {"scale_x": 1.0, "scale_y": 1.0, "alignment": ft.Alignment.BOTTOM_RIGHT}, ft.Colors.PURPLE),
    ]

    boxes = []
    
    for desc, params, color in test_cases:
        # 测试构造函数
        try:
            scale_obj = ft.Scale(**params)
            supported = True
            error_msg = None
            test_log.append(f"✅ {desc}")
        except TypeError as e:
            scale_obj = ft.Scale(scale=1.0)  # 回退到默认
            supported = False
            error_msg = str(e)
            test_log.append(f"❌ {desc}: {error_msg}")
        
        box = ft.Container(
            width=70,
            height=70,
            bgcolor=color,
            border_radius=3,
            scale=scale_obj,
            animate_scale=ft.Animation(duration=600, curve=ft.AnimationCurve.EASE_OUT),
            content=ft.Text(desc[:10], color=ft.Colors.WHITE, size=8),
            alignment=ft.Alignment.CENTER,
            data={"desc": desc, "params": params, "supported": supported, "error": error_msg}
        )
        boxes.append(box)

    # 结果显示
    result_text = ft.Text(
        value="测试结果:\n" + "\n".join(test_log),
        size=10,
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
                # 更新参数，保持 alignment
                params = box.data["params"].copy()
                if "scale" in params:
                    params["scale"] = target
                if "scale_x" in params:
                    params["scale_x"] = target
                if "scale_y" in params:
                    params["scale_y"] = target
                
                try:
                    box.scale = ft.Scale(**params)
                except:
                    # 如果失败，回退到简单缩放
                    box.scale = ft.Scale(scale=target)
            else:
                box.scale = ft.Scale(scale=target)
        
        page.update()

    page.add(
        ft.Text("Scale 参数兼容性测试", size=14, weight=ft.FontWeight.BOLD),
        ft.Text("8种参数组合测试：", size=12),
        result_text,
        ft.Row(
            wrap=True,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=boxes,
        ),
        ft.Button(
            f"切换缩放 (当前: {'1x' if not is_scaled else '2x'})",
            on_click=toggle_scale,
        ),
        ft.Text("关键观察：", size=10, color=ft.Colors.GREY),
        ft.Text("1. scale=1.0, alignment=TOP_LEFT 是否工作？", size=10, color=ft.Colors.GREY),
        ft.Text("2. scale=1.0, alignment=BOTTOM_RIGHT 是否工作？", size=10, color=ft.Colors.GREY),
        ft.Text("3. scale_x/scale_y 与 alignment 是否兼容？", size=10, color=ft.Colors.GREY),
    )


ft.run(main)
