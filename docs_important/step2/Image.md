# Image

Displays an image.

The following popular formats are supported: **JPEG, PNG, SVG, GIF, Animated GIF, WebP, Animated WebP, BMP, and WBMP**.

**Inherits:** `LayoutControl`

## Usage Example

### Basic Image

```python
ft.Image(
    src="https://flet.dev/img/logo.svg",
    width=100,
    height=100,
)

```

---

## Examples

### Image Gallery

```python
import flet as ft

def main(page: ft.Page):
    page.title = "Image Example"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 50

    page.add(
        ft.Image(
            src="app_icon_512.png",
            width=100,
            height=100,
            fit=ft.BoxFit.CONTAIN,
        ),
        gallery := ft.Row(expand=1, wrap=False, scroll=ft.ScrollMode.ALWAYS),
    )

    for i in range(0, 30):
        gallery.controls.append(
            ft.Image(
                src=f"https://picsum.photos/200/200?{i}",
                width=200,
                height=200,
                fit=ft.BoxFit.NONE,
                repeat=ft.ImageRepeat.NO_REPEAT,
                border_radius=ft.BorderRadius.all(10),
            )
        )
    page.update()

ft.run(main)

```

### Fade-in Images with a Placeholder

```python
import time
import flet as ft

def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def show_random(e: ft.Event[ft.Button]):
        image.src = f"https://picsum.photos/320/200?random={time.time()}"  # random

    page.add(
        image := ft.Image(
            src="https://picsum.photos/320/200?random=1",
            width=360,
            height=220,
            fit=ft.BoxFit.COVER,
            # solid blue image as bas64
            placeholder_src="data:image/png;base64,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",  # noqa: E501
            placeholder_fade_out_animation=ft.Animation(
                duration=ft.Duration(milliseconds=900),
                curve=ft.AnimationCurve.EASE_OUT,
            ),
            fade_in_animation=ft.Animation(
                duration=ft.Duration(milliseconds=700),
                curve=ft.AnimationCurve.EASE_IN_OUT,
            ),
        ),
        ft.Button("Show random image", on_click=show_random),
    )

if __name__ == "__main__":
    ft.run(main)

```

### Displaying images from base64 strings and byte data

```python
import base64
import flet as ft

def main(page: ft.Page):
    # image as base64 string
    base64_src = "iVBORw0KGgoAAAANSUhEUgAAABkAAAAgCAYAAADnnNMGAAAACXBIWXMAAAORAAADkQFnq8zdAAAAGXRFWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAAA6dJREFUSImllltoHFUYx3/fzOzm0lt23ZrQ1AQbtBehNpvQohgkBYVo410RwQctNE3Sh0IfiiBoIAjqi6TYrKnFy4O3oiiRavDJFi3mXomIBmOxNZe63ay52GR3Zj4f2sTEzmx3m//TYf7/c35zvgPnO6KqrESXqpq3muocAikv6m+/zytj3ejik1VN21G31YA9CgJ6xC+bMyQZPVCuarciPAMYC99V6Vw5pLbFSibHmlVoRVj9P3cmPBM8tSJI/M6mzabpfoAQ9fIF7WK4bd5vvuFnLGgy2vi0abg94A0AcJGvMq3hDxGRyar9r4F+iLAm0yIiRk8m37tctS1WsrIhhrI30+Srmg+J87OXUf3lWGS1q89dC6ltsSanxk4Aj2QBABii96300g87P/rtlrWr8l+vyDMfdlXSyyEikqxsiOUAQJCBhfHdXRfCq1LSsSlcWG+KBAGStvvrMkgiuv8lUc2mREukPwLUfHG+uTQv8Eown7VL3XlbBxYhf1c17hbVF3MDwA9bts280TnaU1YYqPby07aeFlUlHt27wSQ4CLo+F8AvoTCvHmyKF+ZbEb/M77P2LgvAwmrTHAHflN3KZxVbMC2jMFNOpgPnrMSOhvvFkMezXdwV4ePbtvHtxnJAMQ0j4JtVnO+eLb5oiSlt5HDbv7t1O90lpYCCCKbhfzW5kAIwUAazR0BlfII8Ow0I6uoVmI9MyAMwbMs8CExmDbk4zgu931MyO4OI4KrYflkRjOoTI+uM9d1vjotwKPu9QMk/sxzuO8POiVFcdZ1M2YBVsMEAKOqLvaPIe7mACuw0z/80SMH58SMplxlfiDhVi7dw2pltRhjKBQTQdrSja2KKTfE551NHuaZ0QVPvWYQUn31/Vm2nDvgjF4grVJx6suSvrvrSJ/6cSW2Oz9mf264uNrB806xZ1k/CZ49dUKgDEtlCROX2hfHpx8pGuuo3PpqYulw8fjndOp1yhgtNKRevJ1FyR2Ola+jXAjdnwTkZ6o896GdWdxDw7IxFg+0DpmXchTKSBWQnIuJn9u4j7dt+13UfHXEkXQOcuQ4kMhVtqsgUyPiQiPQfHw1NB2sRjmXKuTg1NwwBYLhtPtQX26eqTwGXPDOqvmcC4Hnwfrrad94GrVsOYTqUTkQY+iTlNe/6O1miSP/x0VB/+wMIDwHn/vtV1iQC4Xv95uUEWVCoL9Y5Z+gdovoyMHUFJHv88jmVy0vTuw7cZNv2YaA61Bfb7ZX5F8SaUv2xwZevAAAAAElFTkSuQmCC"
    # image as bytes
    bytes_src = base64.b64decode(base64_src)

    page.add(
        ft.Image(
            src=base64_src,
            width=100,
            height=100,
        ),
        ft.Image(
            src=bytes_src,
            width=100,
            height=100,
        ),
    )

ft.run(main)

```

### Displaying a static SVG image

```python
import flet as ft

def main(page: ft.Page):
    svg_image = """
<svg version="1.1" id="Layer_1"
    xmlns="http://www.w3.org/2000/svg"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    x="0px" y="0px"
    viewBox="0 0 30 30" style="enable-background:new 0 0 30 30;" xml:space="preserve">
<g>
    <path d="M14.43339,18.88085c2.15923,0,3.91203-1.7476,3.91203-3.91226
        c0-2.15805-1.7528-3.90566-3.91723-3.90566
        c-0.74107,0-1.43221,0.21538-2.02332,0.57576c0.18598-0.05526,0.37562-0.09493,0.58084-0.09493
        c1.09756,0,1.98365,0.88609,1.98365,1.98235c0,1.09248-0.88608,1.98376-1.98365,1.98376
        c-1.09627,0-1.98235-0.88608-1.98235-1.98376c0-0.20499,0.03979-0.39486,0.09493-0.58096
        c-0.36027,0.59135-0.57576,1.28236-0.57576,2.02344C10.52254,17.13325,12.27026,18.88085,14.43339,18.88085z"/>
    <path d="M24.55235,1.00006H5.44812C2.99534,1.00006,
        1,2.99563,1,5.44747v19.10459c0,2.45278,1.99533,4.44788,4.44812,4.44788
        h19.10423c2.45243,0,4.44765-1.9951,4.44765-4.44788V5.44747C29,2.99563,27.00479,1.00006,24.55235,1.00006z
        M27.32951,24.55206
        c0,1.53175-1.246,2.77774-2.77715,2.77774H5.44812c-1.53151,0-2.77751-1.246-2.77751-2.77774v-8.83719h4.08065
        c0.37644,3.90943,3.67563,6.97482,7.67705,6.97482c4.00709,0,7.3065-3.06539,7.68295-6.97482h5.21824V24.55206z
        M8.36366,14.96859
        c0-3.34831,2.7161-6.06418,6.06453-6.06418c3.35469,0,6.07079,2.71587,6.07079,6.06418c0,3.35492-2.7161,6.07079-6.07079,6.07079
        C11.07977,21.03938,8.36366,18.32351,8.36366,14.96859z
        M27.32951,13.75472h-5.28579
        c-0.58568-3.67705-3.77116-6.5006-7.61541-6.5006c-3.83882,0-7.02383,2.82356-7.60951,6.5006H2.67061V5.44747
        c0-1.53128,1.246-2.7768,2.77751-2.7768h19.10423c1.53116,0,2.77715,1.24552,2.77715,2.7768V13.75472z"/>
    <path d="M24.06196,5.11637h-1.75185c-0.48236,0-0.87593,0.39345-0.87593,
        0.87569v1.75186
        c0,0.48225,0.39356,0.87616,0.87593,0.87616h1.75186c0.47776,0,0.87038-0.39392,0.87038-0.87616V5.99205
        C24.93234,5.50982,24.53972,5.11637,24.06196,5.11637z"/>
</g>
</svg>"""

    page.add(
        ft.Image(
            src="https://raw.githubusercontent.com/dnfield/flutter_svg/master/packages/flutter_svg/example/assets/wikimedia/Firefox_Logo_2017.svg",
            width=200,
            height=200,
        ),
        ft.Image(src=svg_image, width=100, height=100, color=ft.Colors.RED),
        ft.Image(src=svg_image, width=100, height=100, color=ft.Colors.BLUE),
        ft.Container(
            bgcolor=ft.Colors.BLACK_87,
            border_radius=5,
            content=ft.Image(
                src=svg_image,
                width=100,
                height=100,
                color=ft.Colors.WHITE,
            ),
        ),
    )

ft.run(main)

```

### Displaying a dynamic SVG image

```python
import asyncio
import flet as ft

async def main(page: ft.Page):
    svg_image = """
<svg width="400" height="400" xmlns="http://www.w3.org/2000/svg">
 <g>
  <ellipse ry="{}" rx="{}" id="svg_1" cy="200" cx="200" stroke="#000" fill="#fff"/>
 </g>
</svg>
"""

    img = ft.Image(src=svg_image.format(0, 0))
    page.add(img)

    for c in range(0, 10):
        for i in range(0, 10):
            img.src = svg_image.format(i * 10, i * 10)
            img.update()
            await asyncio.sleep(0.1)

ft.run(main)

```

### Displaying a Lucide icon

```python
import flet as ft

"""
- Browse Lucide icons: https://lucide.dev/
- Copy SVG and use it as value for `Image.src`
"""

def main(page: ft.Page):
    page.add(
        ft.Image(
            src='<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 7.5V6a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h3.5"></path><path d="M16 2v4"></path><path d="M8 2v4"></path><path d="M3 10h5"></path><path d="M17.5 17.5 16 16.25V14"></path><path d="M22 16a6 6 0 1 1-12 0 6 6 0 0 1 12 0Z"></path></svg>',
            color=ft.Colors.PINK,
        ),
        ft.Image(
            src='<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline></svg>',
            color=ft.Colors.GREEN,
        ),
    )

ft.run(main)

```

---

## Properties

| Property | Type | Default | Attribute Metadata | Description |
| --- | --- | --- | --- | --- |
| **`anti_alias`** | `bool` | `False` | `class-attribute`<br>

<br>`instance-attribute` | Whether to paint the image with anti-aliasing. |
| **`border_radius`** | `BorderRadiusValue` | `None` | `None` | `class-attribute`<br>

<br>`instance-attribute` |
| **`cache_height`** | `int` | `None` | `None` | `class-attribute`<br>

<br>`instance-attribute` |
| **`cache_width`** | `int` | `None` | `None` | `class-attribute`<br>

<br>`instance-attribute` |
| **`color`** | `ColorValue` | `None` | `None` | `class-attribute`<br>

<br>`instance-attribute` |
| **`color_blend_mode`** | `BlendMode` | `None` | `None` | `class-attribute`<br>

<br>`instance-attribute` |
| **`error_content`** | `Control` | `None` | `None` | `class-attribute`<br>

<br>`instance-attribute` |
| **`exclude_from_semantics`** | `bool` | `False` | `class-attribute`<br>

<br>`instance-attribute` | Whether to exclude this image from semantics. |
| **`fade_in_animation`** | `Animation` | `None` | `None` | `class-attribute`<br>

<br>`instance-attribute` |
| **`filter_quality`** | `FilterQuality` | `MEDIUM` | `class-attribute`<br>

<br>`instance-attribute` | The rendering quality of the image. |
| **`fit`** | `BoxFit` | `None` | `None` | `class-attribute`<br>

<br>`instance-attribute` |
| **`gapless_playback`** | `bool` | `False` | `class-attribute`<br>

<br>`instance-attribute` | Whether to continue showing the old image (True), or briefly show nothing (False), when the image provider changes.<br>

<br>Has no effect on svg images. |
| **`placeholder_fade_out_animation`** | `Animation` | `None` | `None` | `class-attribute`<br>

<br>`instance-attribute` |
| **`placeholder_fit`** | `BoxFit` | `None` | `None` | `class-attribute`<br>

<br>`instance-attribute` |
| **`placeholder_src`** | `str` | `bytes` | `None` | `None` |
| **`repeat`** | `ImageRepeat` | `NO_REPEAT` | `class-attribute`<br>

<br>`instance-attribute` | How to paint any portions of the layout bounds not covered by this image. |
| **`semantics_label`** | `str` | `None` | `None` | `class-attribute`<br>

<br>`instance-attribute` |
| **`src`** | `str` | `bytes` | - | `instance-attribute` |