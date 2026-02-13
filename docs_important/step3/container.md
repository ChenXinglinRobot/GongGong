# Container

Allows to decorate a control with background color and border and position it with padding, margin and alignment.

**Inherits:** `LayoutControl`, `AdaptiveControl`

## Examples

### Clickable Container

```python
import flet as ft

def main(page: ft.Page):
    page.title = "Container Example"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.add(
        ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.Container(
                    content=ft.Text("Non clickable"),
                    margin=10,
                    padding=10,
                    alignment=ft.Alignment.CENTER,
                    bgcolor=ft.Colors.AMBER,
                    width=150,
                    height=150,
                    border_radius=10,
                ),
                ft.Container(
                    content=ft.Text("Clickable without Ink"),
                    margin=10,
                    padding=10,
                    alignment=ft.Alignment.CENTER,
                    bgcolor=ft.Colors.GREEN_200,
                    width=150,
                    height=150,
                    border_radius=10,
                    on_click=lambda e: print("Clickable without Ink clicked!"),
                ),
                ft.Container(
                    content=ft.Text("Clickable with Ink"),
                    margin=10,
                    padding=10,
                    alignment=ft.Alignment.CENTER,
                    bgcolor=ft.Colors.CYAN_200,
                    width=150,
                    height=150,
                    border_radius=10,
                    ink=True,
                    on_click=lambda e: print("Clickable with Ink clicked!"),
                ),
                ft.Container(
                    content=ft.Text("Clickable transparent with Ink"),
                    margin=10,
                    padding=10,
                    alignment=ft.Alignment.CENTER,
                    width=150,
                    height=150,
                    border_radius=10,
                    ink=True,
                    on_click=lambda e: print("Clickable transparent with Ink clicked!"),
                ),
            ],
        ),
    )

ft.run(main)

```

### Handling Clicks (Tap, Long Press)

```python
import flet as ft

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    lp_counter = 0
    cl_counter = 0
    td_counter = 0

    def on_click(e):
        nonlocal cl_counter
        cl_counter += 1
        t1.spans[-1] = ft.TextSpan(
            text=f"  {cl_counter}  ",
            style=ft.TextStyle(size=16, bgcolor=ft.Colors.TEAL_300),
        )
        page.update()

    def on_long_press(e):
        nonlocal lp_counter
        lp_counter += 1
        t3.spans[-1] = ft.TextSpan(
            text=f"  {lp_counter}  ",
            style=ft.TextStyle(size=16, bgcolor=ft.Colors.TEAL_300),
        )
        page.update()

    def on_tap_down(e):
        nonlocal td_counter
        td_counter += 1
        t2.spans[-1] = ft.TextSpan(
            text=f"  {td_counter}  ",
            style=ft.TextStyle(size=16, bgcolor=ft.Colors.TEAL_300),
        )
        page.update()

    c = ft.Container(
        bgcolor=ft.Colors.PINK_900,
        alignment=ft.Alignment.CENTER,
        padding=ft.Padding.all(10),
        height=150,
        width=150,
        on_click=on_click,
        on_long_press=on_long_press,
        on_tap_down=on_tap_down,
        content=ft.Text(
            "Press Me!",
            text_align=ft.TextAlign.CENTER,
            style=ft.TextStyle(
                size=30,
                foreground=ft.Paint(
                    color=ft.Colors.BLUE_700,
                    stroke_cap=ft.StrokeCap.BUTT,
                    stroke_width=2,
                    stroke_join=ft.StrokeJoin.BEVEL,
                    style=ft.PaintingStyle.STROKE,
                ),
            ),
            theme_style=ft.TextThemeStyle.DISPLAY_MEDIUM,
        ),
    )
    # ... (Text definitions omitted for brevity, see original source) ...
    
    # Assuming t1, t2, t3 are defined as in the source
    # page.add(c, t1, t3, t2) 

ft.run(main)

```

### Handling Hovers

```python
import flet as ft

def main(page: ft.Page):
    def handle_hover(e: ft.Event[ft.Container]):
        e.control.bgcolor = ft.Colors.BLUE if e.data else ft.Colors.RED
        e.control.update()

    page.add(
        ft.Container(
            width=200,
            height=200,
            bgcolor=ft.Colors.RED,
            ink=False,
            on_hover=handle_hover,
        )
    )

ft.run(main)

```

### Animations

**Basic Animation:**

```python
import flet as ft

def main(page: ft.Page):
    def animate_container(e: ft.Event[ft.Button]):
        container.width = 100 if container.width == 150 else 150
        container.height = 50 if container.height == 150 else 150
        container.bgcolor = (
            ft.Colors.BLUE if container.bgcolor == ft.Colors.RED else ft.Colors.RED
        )
        container.update()

    page.add(
        container := ft.Container(
            width=150,
            height=150,
            bgcolor=ft.Colors.RED,
            animate=ft.Animation(duration=1000, curve=ft.AnimationCurve.BOUNCE_OUT),
        ),
        ft.Button("Animate container", on_click=animate_container),
    )

ft.run(main)

```

**Gradient & Shape Animation:**

```python
import flet as ft

def main(page: ft.Page):
    # ... (Gradient definitions) ...
    message = ft.Text("Animate me!")

    def animate_container(e: ft.Event[ft.Button]):
        # ... (Logic to toggle properties) ...
        container.update()

    page.add(
        container := ft.Container(
            content=message,
            width=250,
            height=250,
            gradient=gradient2,
            alignment=ft.Alignment.TOP_LEFT,
            animate=ft.Animation(duration=1000, curve=ft.AnimationCurve.BOUNCE_OUT),
            border=ft.Border.all(width=2, color=ft.Colors.BLUE),
            border_radius=10,
            padding=10,
        ),
        ft.Button("Animate container", on_click=animate_container),
    )

ft.run(main)

```

### Nested Themes

```python
import flet as ft

def main(page: ft.Page):
    # Yellow page theme with SYSTEM (default) mode
    page.theme = ft.Theme(
        color_scheme_seed=ft.Colors.YELLOW,
    )

    page.add(
        # Page theme
        ft.Container(
            content=ft.Button("Page theme button"),
            bgcolor=ft.Colors.SURFACE_TINT,
            padding=20,
            width=300,
        ),
        # Inherited theme with primary color overridden
        ft.Container(
            theme=ft.Theme(color_scheme=ft.ColorScheme(primary=ft.Colors.PINK)),
            content=ft.Button("Inherited theme button"),
            bgcolor=ft.Colors.SURFACE_TINT,
            padding=20,
            width=300,
        ),
        # Unique always DARK theme
        ft.Container(
            theme=ft.Theme(color_scheme_seed=ft.Colors.INDIGO),
            theme_mode=ft.ThemeMode.DARK,
            content=ft.Button("Unique theme button"),
            bgcolor=ft.Colors.SURFACE_TINT,
            padding=20,
            width=300,
        ),
    )

if __name__ == "__main__":
    ft.run(main)

```

### Size Aware

```python
import flet as ft

def main(page: ft.Page):
    def handle_size_change(e: ft.LayoutSizeChangeEvent[ft.Container]):
        e.control.content.value = f"{int(e.width)} x {int(e.height)}"

    page.add(
        ft.Container(
            expand=True,
            alignment=ft.Alignment.CENTER,
            bgcolor=ft.Colors.BLUE_ACCENT,
            content=ft.Text(color=ft.Colors.WHITE, weight=ft.FontWeight.BOLD),
            size_change_interval=100,
            on_size_change=handle_size_change,
        )
    )

if __name__ == "__main__":
    ft.run(main)

```

---

## Properties

| Property | Type | Default | Description |
| --- | --- | --- | --- |
| **`alignment`** | `Alignment` | `None` | Defines the alignment of the `content` inside the `container`. |
| **`animate`** | `AnimationValue` | `None` | Enables `container` "implicit" animation that gradually changes its values over a period of time. |
| **`bgcolor`** | `ColorValue` | `None` | Defines the background color of this `container`. |
| **`blend_mode`** | `BlendMode` | `MODULATE` | The blend mode applied to the `color` or `gradient` background of the `container`. |
| **`blur`** | `BlurValue` | `None` | Defines how Gaussian blur effect should be applied under this `container`. (See example below) |
| **`border`** | `Border` | `None` | A border to draw above the background color. |
| **`border_radius`** | `BorderRadiusValue` | `None` | The border radius of this `container`. |
| **`clip_behavior`** | `ClipBehavior` | `None`* | Defines how the `content` of this `container` is clipped. <br>

<br> *Defaults to `ANTI_ALIAS` if `border_radius` is not `None`; otherwise `NONE`. |
| **`color_filter`** | `ColorFilter` | `None` | Applies a color filter to this `container`. |
| **`content`** | `Control` | `None` | The content of this `container`. |
| **`dark_theme`** | `Theme` | `None` | Allows setting a nested theme to be used when in dark theme mode for all controls inside the `container` and down its tree. |
| **`foreground_decoration`** | `BoxDecoration` | `None` | The foreground decoration of this `container`. |
| **`gradient`** | `Gradient` | `None` | Defines the gradient background of this `container`. |
| **`ignore_interactions`** | `bool` | `False` | Whether to ignore all interactions with this `container` and its descendants. |
| **`image`** | `DecorationImage` | `None` | An image to paint above the `bgcolor` or `gradient`. If `shape=BoxShape.CIRCLE` then this image is clipped to the circle's boundary; if `border_radius` is not `None` then the image is clipped to the given radii. |
| **`ink`** | `bool` | `False` | `True` to produce ink ripples effect when user clicks this `container`. |
| **`ink_color`** | `ColorValue` | `None` | The splash color of the ink response. |
| **`padding`** | `PaddingValue` | `None` | Empty space to inscribe inside a `container` decoration (background, border). The child control is placed inside this padding. |
| **`shadow`** | `BoxShadowValue` | `None` | The shadow(s) below this `container`. |
| **`shape`** | `BoxShape` | `RECTANGLE` | Sets the shape of this `container`. |
| **`theme`** | `Theme` | `None` | Allows setting a nested theme for all controls inside this `container` and down its tree. |
| **`theme_mode`** | `ThemeMode` | `SYSTEM` | "Resets" parent theme and creates a new, unique scheme for all controls inside the `container`. Otherwise the styles defined in `container`'s `theme` property override corresponding styles from the parent, inherited theme. |
| **`url`** | `str` | `Url` | `None` |

### Blur Example

```python
ft.Container(
    width=50,
    height=50,
    blur=ft.Blur(10, 0, ft.BlurTileMode.MIRROR),
    bgcolor="#44CCCCCC",
)

```

---

## Events

| Event | Type | Description |
| --- | --- | --- |
| **`on_click`** | `ControlEventHandler` | Called when a user clicks the `container`. It will not be called if this `container` is long pressed. |
| **`on_hover`** | `ControlEventHandler` | Called when a mouse pointer enters or exists the `container` area. The `data` property is `True` when entering and `False` when exiting. |
| **`on_long_press`** | `ControlEventHandler` | Called when this `container` is long-pressed. |
| **`on_tap_down`** | `EventHandler` | Called when a user clicks the `container` with or without a long press. |