# ListView

A scrollable list of controls arranged linearly.

`ListView` is the most commonly used scrolling control. It displays its children one after another in the scroll direction. In the cross axis, the children are required to fill the `ListView`.

**Inherits:** `LayoutControl`, `ScrollableControl`, `AdaptiveControl`

## Usage Example

### Basic List View

```python
import flet as ft

ft.ListView(
    controls=[ft.Text(f"Item {i}") for i in range(1, 6)],
)

```

---

## Examples

### Auto-scrolling and dynamical items addition

```python
import asyncio
import flet as ft

async def main(page: ft.Page):
    def handle_switch_change(e: ft.Event[ft.Switch]):
        lv.auto_scroll = not lv.auto_scroll
        page.update()

    lv = ft.ListView(
        spacing=10,
        padding=20,
        width=150,
        auto_scroll=True,
        controls=[
            ft.Text(f"Line {i}", color=ft.Colors.ON_SECONDARY) for i in range(0, 60)
        ],
    )

    page.add(
        ft.Row(
            expand=True,
            vertical_alignment=ft.CrossAxisAlignment.START,
            controls=[
                ft.Container(
                    content=lv,
                    bgcolor=ft.Colors.GREY_500,
                ),
                ft.Switch(
                    thumb_icon=ft.Icons.LIST_OUTLINED,
                    value=True,
                    label="Auto-scroll",
                    label_position=ft.LabelPosition.RIGHT,
                    on_change=handle_switch_change,
                ),
            ],
        )
    )

    # add a new item to the ListView every 1 second
    for i in range(len(lv.controls), 120):
        await asyncio.sleep(1)
        lv.controls.append(ft.Text(f"Line {i}", color=ft.Colors.ON_SECONDARY))
        page.update()

ft.run(main)

```

---

## Properties

| Property | Type | Default | Attribute Metadata | Description |
| --- | --- | --- | --- | --- |
| **`build_controls_on_demand`** | `bool` | `True` | `class-attribute`<br>

<br>`instance-attribute` | Whether the `controls` should be built lazily/on-demand. Useful for large lists. |
| **`cache_extent`** | `Number` | `None` | `None` | `class-attribute`<br>

<br>`instance-attribute` |
| **`clip_behavior`** | `ClipBehavior` | `HARD_EDGE` | `class-attribute`<br>

<br>`instance-attribute` | How to clip the `controls`. |
| **`controls`** | `list[Control]` | `[]` | `class-attribute`<br>

<br>`instance-attribute` | A list of Controls to display inside `ListView`. |
| **`divider_thickness`** | `Number` | `0` | `class-attribute`<br>

<br>`instance-attribute` | If greater than `0`, a `Divider` is used as spacing between list view items. |
| **`first_item_prototype`** | `bool` | `False` | `class-attribute`<br>

<br>`instance-attribute` | Whether the dimensions of the first item should be used as a "prototype" for all other items (same height/width). |
| **`horizontal`** | `bool` | `False` | `class-attribute`<br>

<br>`instance-attribute` | Whether to layout the `controls` horizontally. |
| **`item_extent`** | `Number` | `None` | `None` | `class-attribute`<br>

<br>`instance-attribute` |
| **`padding`** | `PaddingValue` | `None` | `None` | `class-attribute`<br>

<br>`instance-attribute` |
| **`prototype_item`** | `Control` | `None` | `None` | `class-attribute`<br>

<br>`instance-attribute` |
| **`reverse`** | `bool` | `False` | `class-attribute`<br>

<br>`instance-attribute` | Whether the scroll view scrolls in the reading direction.<br>

<br>(e.g., Right-to-Left if True and horizontal). |
| **`semantic_child_count`** | `int` | `None` | `None` | `class-attribute`<br>

<br>`instance-attribute` |
| **`spacing`** | `Number` | `0` | `class-attribute`<br>

<br>`instance-attribute` | The height of the divider between the `controls`. |