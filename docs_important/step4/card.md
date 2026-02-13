# Card

A Material Design card: a panel with slightly rounded corners and an elevation shadow.

**Inherits:** `LayoutControl`, `AdaptiveControl`

## Usage Example

### Basic Card

```python
import flet as ft

ft.Card(
    shadow_color=ft.Colors.ON_SURFACE_VARIANT,
    content=ft.Container(
        width=400,
        padding=10,
        content=ft.ListTile(
            bgcolor=ft.Colors.GREY_400,
            leading=ft.Icon(ft.Icons.FOREST),
            title=ft.Text("Card Name"),
        ),
    ),
)

```

---

## Examples

### Card with Buttons (Live Example)

```python
import flet as ft

def main(page: ft.Page):
    page.title = "Card Example"
    page.theme_mode = ft.ThemeMode.LIGHT

    page.add(
        ft.Card(
            shadow_color=ft.Colors.ON_SURFACE_VARIANT,
            content=ft.Container(
                width=400,
                padding=10,
                content=ft.Column(
                    controls=[
                        ft.ListTile(
                            bgcolor=ft.Colors.GREY_400,
                            leading=ft.Icon(ft.Icons.ALBUM),
                            title=ft.Text("The Enchanted Nightingale"),
                            subtitle=ft.Text(
                                "Music by Julie Gable. Lyrics by Sidney Stein."
                            ),
                        ),
                        ft.Row(
                            alignment=ft.MainAxisAlignment.END,
                            controls=[
                                ft.TextButton("Buy tickets"),
                                ft.TextButton("Listen"),
                            ],
                        ),
                    ]
                ),
            ),
        )
    )

if __name__ == "__main__":
    ft.run(main)

```

---

## Properties

| Property | Type | Default | Attribute Metadata | Description |
| --- | --- | --- | --- | --- |
| **`bgcolor`** | `ColorValue` | `None` | `None` | `class-attribute`<br>

<br>`instance-attribute` |
| **`clip_behavior`** | `ClipBehavior` | `None` | `None`* | `class-attribute`<br>

<br>`instance-attribute` |
| **`content`** | `Control` | `None` | `None` | `class-attribute`<br>

<br>`instance-attribute` |
| **`elevation`** | `Number` | `None` | `None`* | `class-attribute`<br>

<br>`instance-attribute` |
| **`semantic_container`** | `bool` | `True` | `class-attribute`<br>

<br>`instance-attribute` | Whether this card represents a single semantic container, or a collection of individual semantic nodes. |
| **`shadow_color`** | `ColorValue` | `None` | `None`* | `class-attribute`<br>

<br>`instance-attribute` |
| **`shape`** | `OutlinedBorder` | `None` | `None`* | `class-attribute`<br>

<br>`instance-attribute` |
| **`show_border_on_foreground`** | `bool` | `True` | `class-attribute`<br>

<br>`instance-attribute` | Whether the shape of the border should be painted in front of the `content` or behind. |
| **`variant`** | `CardVariant` | `ELEVATED` | `class-attribute`<br>

<br>`instance-attribute` | Defines the card variant to be used. |