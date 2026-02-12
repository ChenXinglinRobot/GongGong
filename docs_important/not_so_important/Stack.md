# Stack

Positions its children on top of each other, following a **LIFO** (Last In First Out) order.

This control is useful if you want to overlap several children in a simple way. For example, having some text and an image, overlaid with a gradient and a button attached to the bottom.

`Stack` is also useful if you want to implement [implicit animations](https://flet.dev/docs/guides/python/animations/) that require knowing the absolute position of a target value.

**Inherits:** `LayoutControl`, `AdaptiveControl`

## Usage Example

### Basic Stack (Text over Image)

```python
import flet as ft

ft.Stack(
    width=300,
    height=300,
    controls=[
        ft.Image(
            src="https://picsum.photos/300/300",
            width=300,
            height=300,
            fit=ft.BoxFit.CONTAIN,
        ),
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Text(
                    value="Image title",
                    color=ft.Colors.SURFACE_TINT,
                    size=40,
                    weight=ft.FontWeight.BOLD,
                    opacity=0.5,
                )
            ],
        ),
    ],
)

```

---

## Examples

### Avatar with Online Status

```python
import flet as ft

def main(page: ft.Page):
    page.add(
        ft.Stack(
            width=40,
            height=40,
            controls=[
                ft.CircleAvatar(
                    foreground_image_src="https://avatars.githubusercontent.com/u/5041459?s=88&v=4"
                ),
                ft.Container(
                    content=ft.CircleAvatar(bgcolor=ft.Colors.GREEN, radius=5),
                    alignment=ft.Alignment.BOTTOM_LEFT,
                ),
            ],
        )
    )

if __name__ == "__main__":
    ft.run(main)

```

### Absolute Positioning

```python
import flet as ft

def main(page: ft.Page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    page.add(
        ft.Container(
            border_radius=8,
            padding=5,
            width=200,
            height=200,
            bgcolor=ft.Colors.BLACK,
            content=ft.Stack(
                controls=[
                    ft.Container(
                        width=20,
                        height=20,
                        bgcolor=ft.Colors.RED,
                        border_radius=5,
                    ),
                    ft.Container(
                        width=20,
                        height=20,
                        bgcolor=ft.Colors.YELLOW,
                        border_radius=5,
                        right=0,
                    ),
                    ft.Container(
                        width=20,
                        height=20,
                        bgcolor=ft.Colors.BLUE,
                        border_radius=5,
                        right=0,
                        bottom=0,
                    ),
                    ft.Container(
                        width=20,
                        height=20,
                        bgcolor=ft.Colors.GREEN,
                        border_radius=5,
                        left=0,
                        bottom=0,
                    ),
                    ft.Column(
                        left=85,
                        top=85,
                        controls=[
                            ft.Container(
                                width=20,
                                height=20,
                                bgcolor=ft.Colors.PURPLE,
                                border_radius=5,
                            )
                        ],
                    ),
                ]
            ),
        )
    )

if __name__ == "__main__":
    ft.run(main)

```

---

## Properties

| Property | Type | Default | Description |
| --- | --- | --- | --- |
| **`alignment`** | `Alignment` | `None` | `None` |
| **`clip_behavior`** | `ClipBehavior` | `HARD_EDGE` | The content will be clipped (or not) according to this option. |
| **`controls`** | `list[Control]` | `[]` | A list of Controls to display. <br>

<br>For the display order, it follows the order of the list, so the last control in the list will be displayed on top (**LIFO** - Last In First Out). |
| **`fit`** | `StackFit` | `LOOSE` | How to size the non-positioned controls. |