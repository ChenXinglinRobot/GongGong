# LayoutControl

**Inherits:** `Control`

Base class for layout-related controls.

## Properties

| Property | Type | Default | Attribute Metadata | Description |
| --- | --- | --- | --- | --- |
| **`align`** | `Alignment` | `None` | `None` | `class-attribute`<br>

<br>`instance-attribute` |
| **`animate_align`** | `AnimationValue` | `None` | `None` | `class-attribute`<br>

<br>`instance-attribute` |
| **`animate_margin`** | `AnimationValue` | `None` | `None` | `class-attribute`<br>

<br>`instance-attribute` |
| **`animate_offset`** | `AnimationValue` | `None` | `None` | `class-attribute`<br>

<br>`instance-attribute` |
| **`animate_opacity`** | `AnimationValue` | `None` | `None` | `class-attribute`<br>

<br>`instance-attribute` |
| **`animate_position`** | `AnimationValue` | `None` | `None` | `class-attribute`<br>

<br>`instance-attribute` |
| **`animate_rotation`** | `AnimationValue` | `None` | `None` | `class-attribute`<br>

<br>`instance-attribute` |
| **`animate_scale`** | `AnimationValue` | `None` | `None` | `class-attribute`<br>

<br>`instance-attribute` |
| **`animate_size`** | `AnimationValue` | `None` | `None` | `class-attribute`<br>

<br>`instance-attribute` |
| **`aspect_ratio`** | `Number` | `None` | `None` | `class-attribute`<br>

<br>`instance-attribute` |
| **`bottom`** | `Number` | `None` | `None` | `class-attribute`<br>

<br>`instance-attribute` |
| **`height`** | `Number` | `None` | `None` | `class-attribute`<br>

<br>`instance-attribute` |
| **`left`** | `Number` | `None` | `None` | `class-attribute`<br>

<br>`instance-attribute` |
| **`margin`** | `MarginValue` | `None` | `None` | `class-attribute`<br>

<br>`instance-attribute` |
| **`offset`** | `OffsetValue` | `None` | `None` | `class-attribute`<br>

<br>`instance-attribute` |
| **`right`** | `Number` | `None` | `None` | `class-attribute`<br>

<br>`instance-attribute` |
| **`rotate`** | `RotateValue` | `None` | `None` | `class-attribute`<br>

<br>`instance-attribute` |
| **`scale`** | `ScaleValue` | `None` | `None` | `class-attribute`<br>

<br>`instance-attribute` |
| **`size_change_interval`** | `int` | `10` | `class-attribute`<br>

<br>`instance-attribute` | Sampling interval in milliseconds for `on_size_change` event. Set to `0` for immediate updates. |
| **`top`** | `Number` | `None` | `None` | `class-attribute`<br>

<br>`instance-attribute` |
| **`width`** | `Number` | `None` | `None` | `class-attribute`<br>

<br>`instance-attribute` |

> **Note 1 (Positioning):** `top`, `bottom`, `left`, and `right` properties are effective **only** if this control is a descendant of a `Stack` control or the `Page.overlay` list.

---

## Detailed Usage & Examples

### `offset`

The translation is expressed as an `Offset` scaled to the control's size.

* `Offset(x=0.25, y=0)` results in a horizontal translation of one quarter the width of this control.

**Example:**
The following example displays a container at `0, 0` (top left corner) of a stack because the transform applies `-1 * 100` horizontal and `-1 * 100` vertical translation (offset * control's size).

```python
import flet as ft

def main(page: ft.Page):
    page.add(
        ft.Stack(
            width=1000,
            height=1000,
            controls=[
                ft.Container(
                    bgcolor=ft.Colors.RED,
                    width=100,
                    height=100,
                    left=100,
                    top=100,
                    offset=ft.Offset(-1, -1),
                )
            ],
        )
    )

ft.run(main)

```

### `rotate`

Transforms this control using a rotation around its center. The value can be:

* **`number`**: Rotation in clockwise radians (e.g., `math.pi * 2` is 360°, `pi / 2` is 90°).
* **`Rotate` object**: Allows specifying rotation `angle` as well as `alignment` (the location of the rotation center).

**Example:**

```python
ft.Image(
    src="https://picsum.photos/100/100",
    width=100,
    height=100,
    border_radius=5,
    rotate=ft.Rotate(angle=0.25 * 3.14, alignment=ft.Alignment.CENTER_LEFT)
)

```

### `scale`

Scales this control along the 2D plane. Default is `1.0` (no-scale).

* `0.5`: Makes control twice as small.
* `2.0`: Makes control twice as large.
* **`Scale` object**: Different scale multipliers can be specified for `x` and `y` axis. (Note: Specify either `scale` OR `scale_x`/`scale_y`, not both).

**Example:**

```python
ft.Image(
    src="https://picsum.photos/100/100",
    width=100,
    height=100,
    border_radius=5,
    scale=ft.Scale(scale_x=2, scale_y=0.5)
)

```

---

## Events

| Event | Attribute Metadata | Description |
| --- | --- | --- |
| **`on_animation_end`** | `class-attribute`<br>

<br>`instance-attribute` | Called when animation completes. Can be used to chain multiple animations.<br>

<br>The `data` property of the event handler argument contains the name of the animation. |
| **`on_size_change`** | `class-attribute`<br>

<br>`instance-attribute` | Called when the size of this control changes.<br>

<br>`size_change_interval` defines how often this event is called. |