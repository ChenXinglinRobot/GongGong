# Alignment

Defines an alignment relative to the center.

## Properties

| Property | Type | Attribute Metadata | Description |
| --- | --- | --- | --- |
| **`x`** | `Number` | `instance-attribute` | Represents the horizontal distance from the center.<br>

<br>Value ranges between `-1.0` and `1.0` inclusive. |
| **`y`** | `Number` | `instance-attribute` | Represents the vertical distance from the center.<br>

<br>Value ranges between `-1.0` and `1.0` inclusive. |
| **`BOTTOM_CENTER`** | `AlignmentProperty` | `class-attribute` | Represents the bottom center.<br>

<br>Equivalent to `Alignment(0.0, 1.0)`. |
| **`BOTTOM_LEFT`** | `AlignmentProperty` | `class-attribute` | Represents the bottom left corner.<br>

<br>Equivalent to `Alignment(-1.0, 1.0)`. |
| **`BOTTOM_RIGHT`** | `AlignmentProperty` | `class-attribute` | Represents the bottom right corner.<br>

<br>Equivalent to `Alignment(1.0, 1.0)`. |
| **`CENTER`** | `AlignmentProperty` | `class-attribute` | Represents the center.<br>

<br>Equivalent to `Alignment(0.0, 0.0)`. |
| **`CENTER_LEFT`** | `AlignmentProperty` | `class-attribute` | Represents the center left.<br>

<br>Equivalent to `Alignment(-1.0, 0.0)`. |
| **`CENTER_RIGHT`** | `AlignmentProperty` | `class-attribute` | Represents the center right.<br>

<br>Equivalent to `Alignment(1.0, 0.0)`. |
| **`TOP_CENTER`** | `AlignmentProperty` | `class-attribute` | Represents the top center.<br>

<br>Equivalent to `Alignment(0.0, -1.0)`. |
| **`TOP_LEFT`** | `AlignmentProperty` | `class-attribute` | Represents the top left corner.<br>

<br>Equivalent to `Alignment(-1.0, -1.0)`. |
| **`TOP_RIGHT`** | `AlignmentProperty` | `class-attribute` | Represents the top right corner.<br>

<br>Equivalent to `Alignment(1.0, -1.0)`. |

---

## Methods

### `copy`

```python
copy(*, x: Number | None = None, y: Number | None = None) -> Alignment

```

Returns a copy of this object with the specified properties overridden.

---

## Examples

### Example 1: Containers with different alignments

```python
import flet as ft

def main(page: ft.Page):
    page.title = "Containers with different alignments"

    page.add(
        ft.Row(
            controls=[
                ft.Container(
                    content=ft.Button("Center"),
                    bgcolor=ft.Colors.AMBER,
                    padding=15,
                    alignment=ft.Alignment.CENTER,
                    width=150,
                    height=150,
                ),
                ft.Container(
                    content=ft.Button("Top left"),
                    bgcolor=ft.Colors.AMBER,
                    padding=15,
                    alignment=ft.Alignment.TOP_LEFT,
                    width=150,
                    height=150,
                ),
                ft.Container(
                    content=ft.Button("-0.5, -0.5"),
                    bgcolor=ft.Colors.AMBER,
                    padding=15,
                    alignment=ft.alignment.Alignment(-0.5, -0.5),
                    width=150,
                    height=150,
                ),
            ]
        )
    )

ft.run(main)

```