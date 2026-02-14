# HapticFeedback

Allows access to the haptic feedback interface on the device.

**Inherits:** `Service`

## Examples

### Basic Example

```python
import flet as ft

def main(page: ft.Page):
    hf = ft.HapticFeedback()

    async def heavy_impact(e):
        await hf.heavy_impact()

    async def medium_impact(e):
        await hf.medium_impact()

    async def light_impact(e):
        await hf.light_impact()

    async def vibrate(e):
        await hf.vibrate()

    page.add(
        ft.Button("Heavy impact", on_click=heavy_impact),
        ft.Button("Medium impact", on_click=medium_impact),
        ft.Button("Light impact", on_click=light_impact),
        ft.Button("Vibrate", on_click=vibrate),
    )

ft.run(main)

```

---

## Methods

| Method | Description |
| --- | --- |
| **`heavy_impact`** | Provides a haptic feedback corresponding a collision impact with a heavy mass. |
| **`light_impact`** | Provides a haptic feedback corresponding a collision impact with a light mass. |
| **`medium_impact`** | Provides a haptic feedback corresponding a collision impact with a medium mass. |
| **`selection_click`** | TBD |
| **`vibrate`** | Provides vibration haptic feedback to the user for a short duration. |