# GestureDetector

A control that detects gestures.
Attempts to recognize gestures that correspond to its non-None callbacks.
If this control has a `content`, it defers to that child control for its sizing behavior, else it grows to fit the parent instead.

**Inherits:** `LayoutControl`, `AdaptiveControl`

## Examples

### Handling Events

```python
import flet as ft

def main(page: ft.Page):
    page.add(
        ft.GestureDetector(
            content=ft.Container(bgcolor=ft.Colors.GREEN, width=200, height=200),
            hover_interval=50,
            on_tap=lambda e: print("Tap"),
            on_tap_down=lambda e: print("Tap Down"),
            on_tap_up=lambda e: print("Tap Up"),
            on_secondary_tap=lambda e: print("Secondary Tap"),
            on_secondary_tap_down=lambda e: print("Secondary Tap Down"),
            on_secondary_tap_up=lambda e: print("Secondary Tap Up"),
            on_long_press_start=lambda e: print("Long Press Start"),
            on_long_press_end=lambda e: print("Long Press End"),
            on_secondary_long_press_start=lambda e: print("Sec Long Press Start"),
            on_secondary_long_press_end=lambda e: print("Sec Long Press End"),
            on_double_tap=lambda e: print("Double Tap"),
            on_double_tap_down=lambda e: print("Double Tap Down"),
            on_pan_start=lambda e: print("Pan Start"),
            on_pan_update=lambda e: print("Pan Update"),
            on_pan_end=lambda e: print("Pan End"),
            on_hover=lambda e: print("Hover"),
            on_enter=lambda e: print("Enter"),
            on_exit=lambda e: print("Exit"),
        )
    )

ft.run(main)

```

### Draggable Containers

The following example demonstrates how a control can be freely dragged inside a `Stack`.
It shows that `GestureDetector` can have a child control (blue container) or be nested inside another control (yellow container).

```python
import flet as ft

def main(page: ft.Page):
    def handle_pan_update1(e: ft.DragUpdateEvent[ft.GestureDetector]):
        container = e.control.parent
        container.top = max(0.0, container.top + e.local_delta.y)
        container.left = max(0.0, container.left + e.local_delta.x)
        container.update()

    def handle_pan_update2(e: ft.DragUpdateEvent[ft.GestureDetector]):
        e.control.top = max(0.0, e.control.top + e.local_delta.y)
        e.control.left = max(0.0, e.control.left + e.local_delta.x)
        e.control.update()

    page.add(
        ft.Stack(
            width=1000,
            height=500,
            controls=[
                ft.Container(
                    bgcolor=ft.Colors.AMBER,
                    width=50,
                    height=50,
                    left=0,
                    top=0,
                    content=ft.GestureDetector(
                        mouse_cursor=ft.MouseCursor.MOVE,
                        drag_interval=50,
                        on_pan_update=handle_pan_update1,
                    ),
                ),
                ft.GestureDetector(
                    mouse_cursor=ft.MouseCursor.MOVE,
                    drag_interval=10,
                    on_vertical_drag_update=handle_pan_update2,
                    left=100,
                    top=100,
                    content=ft.Container(bgcolor=ft.Colors.BLUE, width=50, height=50),
                ),
            ],
        )
    )

ft.run(main)

```

### Window Drag Area

```python
import flet as ft

def main(page: ft.Page):
    def on_pan_update(e: ft.DragUpdateEvent[ft.GestureDetector]):
        page.window.left += e.global_delta.x
        page.window.top += e.global_delta.y
        page.update()

    page.add(
        ft.Stack(
            width=1000,
            height=500,
            controls=[
                ft.GestureDetector(
                    mouse_cursor=ft.MouseCursor.MOVE,
                    on_pan_update=on_pan_update,
                    left=200,
                    top=200,
                    content=ft.Container(bgcolor=ft.Colors.PINK, width=50, height=50),
                ),
            ],
        )
    )

ft.run(main)

```

### Mouse Cursors

```python
import random
import flet as ft

def main(page: ft.Page):
    def on_pan_update(event: ft.DragUpdateEvent[ft.GestureDetector]):
        container.top = max(0.0, container.top + event.delta_y)
        container.left = max(0.0, container.left + event.delta_x)
        container.update()

    gesture_detector = ft.GestureDetector(
        mouse_cursor=ft.MouseCursor.BASIC,
        drag_interval=50,
        on_pan_update=on_pan_update,
    )
    container = ft.Container(
        content=gesture_detector,
        bgcolor=ft.Colors.AMBER,
        width=150,
        height=150,
        left=0,
        top=0,
    )

    def handle_button_click(e: ft.Event[ft.Button]):
        gesture_detector.mouse_cursor = random.choice(list(ft.MouseCursor))
        text.value = f"Mouse Cursor:  {gesture_detector.mouse_cursor}"
        page.update()

    page.add(
        ft.Stack(controls=[container], width=1000, height=500),
        ft.Button("Change mouse Cursor", on_click=handle_button_click),
        text := ft.Text(f"Mouse Cursor:  {gesture_detector.mouse_cursor}"),
    )

ft.run(main)

```

---

## Properties

| Property | Type | Default | Description |
| --- | --- | --- | --- |
| **`allowed_devices`** | `list[PointerDeviceType]` | `None` | TBD |
| **`content`** | `Control` | `None` | A child Control contained by the gesture detector. |
| **`drag_interval`** | `int` | `0` | Throttling in milliseconds for horizontal drag, vertical drag and pan update events. <br>

<br> `0` means no throttling (smoothest tracking). |
| **`exclude_from_semantics`** | `bool` | `False` | TBD |
| **`hover_interval`** | `int` | `0` | Throttling in milliseconds for `on_hover` event. |
| **`mouse_cursor`** | `MouseCursor` | `None` | The mouse cursor for mouse pointers that are hovering over the control. |
| **`multi_tap_touches`** | `int` | `0` | The minimum number of pointers to trigger `on_multi_tap` event. |
| **`trackpad_scroll_causes_scale`** | `bool` | `False` | TBD |

---

## Events

### Tap Events (Primary)

| Event | Type | Description |
| --- | --- | --- |
| **`on_tap`** | `TapEvent` | Called when a tap with a primary button has occurred. |
| **`on_tap_down`** | `TapEvent` | Called when a pointer that might cause a tap with a primary button has contacted the screen. |
| **`on_tap_up`** | `TapEvent` | Called when a pointer that will trigger a tap with a primary button has stopped contacting the screen. |
| **`on_tap_cancel`** | `ControlEvent` | The pointer that previously triggered `on_tap_down` will not end up causing a tap. |
| **`on_tap_move`** | `TapMoveEvent` | Called when a pointer that triggered a tap has moved. |
| **`on_double_tap`** | `ControlEvent` | The user has tapped the screen with a primary button at the same location twice in quick succession. |
| **`on_double_tap_down`** | `TapEvent` | Called when a pointer that might cause a double tap has contacted the screen. |
| **`on_double_tap_cancel`** | `ControlEvent` | The pointer sequence that was expected to cause a double tap will not do so. |
| **`on_multi_tap`** | `TapEvent` | Called when multiple pointers contacted the screen. |

### Secondary & Tertiary Tap Events

| Event | Type | Description |
| --- | --- | --- |
| **`on_secondary_tap`** | `ControlEvent` | A tap with a secondary button has occurred. |
| **`on_secondary_tap_down`** | `TapEvent` | Called when a pointer that might cause a tap with a secondary button has contacted the screen. |
| **`on_secondary_tap_up`** | `TapEvent` | Called when a pointer that will trigger a tap with a secondary button has stopped contacting the screen. |
| **`on_secondary_tap_cancel`** | `ControlEvent` | The pointer that previously triggered `on_secondary_tap_down` will not end up causing a tap. |
| **`on_tertiary_tap_down`** | `TapEvent` | Called when a pointer that might cause a tap with a tertiary button has contacted the screen. |
| **`on_tertiary_tap_up`** | `TapEvent` | Called when a pointer that will trigger a tap with a tertiary button has stopped contacting the screen. |
| **`on_tertiary_tap_cancel`** | `ControlEvent` | The pointer that previously triggered `on_tertiary_tap_down` will not end up causing a tap. |

### Long Press Events

| Event | Type | Description |
| --- | --- | --- |
| **`on_long_press`** | `ControlEvent` | Called when a long press gesture with a primary button has been recognized. |
| **`on_long_press_start`** | `LongPressStartEvent` | Triggered when a pointer has remained in contact with the screen for a long period. |
| **`on_long_press_down`** | `LongPressDownEvent` | Called when a pointer that might cause a long press with a primary button has contacted the screen. |
| **`on_long_press_move_update`** | `LongPressMoveUpdateEvent` | Called when, after a long press has been accepted, the pointer moves. |
| **`on_long_press_end`** | `LongPressEndEvent` | Called when a pointer that has triggered a long-press with a primary button has stopped contacting the screen. |
| **`on_long_press_up`** | `ControlEvent` | Called when a pointer that has triggered a long press with a primary button is no longer in contact with the screen. |
| **`on_long_press_cancel`** | `ControlEvent` | The pointer that previously triggered `on_long_press_down` will not end up causing a long-press. |
| **`on_multi_long_press`** | `LongPressEndEvent` | Called when a long press gesture with multiple pointers has been recognized. |

### Secondary & Tertiary Long Press Events

| Event | Type | Description |
| --- | --- | --- |
| **`on_secondary_long_press`** | `ControlEvent` | Called when a long press gesture with a secondary button has been recognized. |
| **`on_secondary_long_press_start`** | `LongPressStartEvent` | Triggered when a pointer (secondary) has remained in contact for a long period. |
| **`on_secondary_long_press_down`** | `LongPressDownEvent` | Called when a pointer that might cause a long press with a secondary button has contacted the screen. |
| **`on_secondary_long_press_move_update`** | `LongPressMoveUpdateEvent` | Called when, after a secondary long press has been accepted, the pointer moves. |
| **`on_secondary_long_press_end`** | `LongPressEndEvent` | Called when a pointer that has triggered a long-press with a secondary button has stopped contacting the screen. |
| **`on_secondary_long_press_up`** | `ControlEvent` | Called when a pointer that has triggered a long press with a secondary button is no longer in contact. |
| **`on_secondary_long_press_cancel`** | `ControlEvent` | The pointer that previously triggered `on_secondary_long_press_down` will not cause a long-press. |
| **`on_tertiary_long_press`** | `ControlEvent` | Called when a long press gesture with a tertiary button has been recognized. |
| **`on_tertiary_long_press_start`** | `LongPressStartEvent` | Triggered when a pointer (tertiary) has remained in contact for a long period. |
| **`on_tertiary_long_press_down`** | `LongPressDownEvent` | Called when a pointer that might cause a long press with a tertiary button has contacted the screen. |
| **`on_tertiary_long_press_move_update`** | `LongPressMoveUpdateEvent` | Called when, after a tertiary long press has been accepted, the pointer moves. |
| **`on_tertiary_long_press_end`** | `LongPressEndEvent` | Called when a pointer that has triggered a long-press with a tertiary button has stopped contacting the screen. |
| **`on_tertiary_long_press_up`** | `ControlEvent` | Called when a pointer that has triggered a long press with a tertiary button is no longer in contact. |
| **`on_tertiary_long_press_cancel`** | `ControlEvent` | The pointer that previously triggered `on_tertiary_long_press_down` will not cause a long-press. |

### Drag & Pan Events

| Event | Type | Description |
| --- | --- | --- |
| **`on_pan_start`** | `DragStartEvent` | Called when a pointer has contacted the screen and has begun to move. |
| **`on_pan_down`** | `DragDownEvent` | Called when a pointer has contacted the screen and might begin to move. |
| **`on_pan_update`** | `DragUpdateEvent` | Called when a pointer that is in contact with the screen and moving has moved again. |
| **`on_pan_end`** | `DragEndEvent` | Called when a pointer is no longer in contact and was moving at a specific velocity. |
| **`on_pan_cancel`** | `ControlEvent` | The pointer that previously triggered `on_pan_down` will not end up causing a pan gesture. |
| **`on_horizontal_drag_start`** | `DragStartEvent` | Called when a pointer has contacted the screen with a primary button and has begun to move horizontally. |
| **`on_horizontal_drag_down`** | `DragDownEvent` | Called when a pointer has contacted the screen and might begin to move horizontally. |
| **`on_horizontal_drag_update`** | `DragUpdateEvent` | Called when a pointer in contact with the screen has moved in the horizontal direction. |
| **`on_horizontal_drag_end`** | `DragEndEvent` | Called when a pointer moving horizontally is no longer in contact. |
| **`on_horizontal_drag_cancel`** | `ControlEvent` | The pointer that previously triggered `on_horizontal_drag_down` will not cause a horizontal drag. |
| **`on_vertical_drag_start`** | `DragStartEvent` | Called when a pointer has contacted the screen and has begun to move vertically. |
| **`on_vertical_drag_down`** | `DragDownEvent` | Called when a pointer has contacted the screen and might begin to move vertically. |
| **`on_vertical_drag_update`** | `DragUpdateEvent` | Called when a pointer in contact with the screen has moved in the vertical direction. |
| **`on_vertical_drag_end`** | `DragEndEvent` | Called when a pointer moving vertically is no longer in contact. |
| **`on_vertical_drag_cancel`** | `ControlEvent` | The pointer that previously triggered `on_vertical_drag_down` will not cause a vertical drag. |
| **`on_right_pan_start`** | `PointerEvent` | Pointer has contacted the screen while secondary button pressed and has begun to move. |
| **`on_right_pan_update`** | `PointerEvent` | A pointer (secondary button) in contact with the screen and moving has moved again. |
| **`on_right_pan_end`** | `PointerEvent` | A pointer with secondary button pressed is no longer in contact. |

### Force Press, Hover & Scale Events

| Event | Type | Description |
| --- | --- | --- |
| **`on_force_press_start`** | `ForcePressEvent` | Called when a pointer has pressed with a force exceeding the start pressure. |
| **`on_force_press_peak`** | `ForcePressEvent` | Called when a pointer has pressed with a force exceeding the peak pressure. |
| **`on_force_press_update`** | `ForcePressEvent` | Called for each update after a force press has started. |
| **`on_force_press_end`** | `ForcePressEvent` | Called when the pointer that triggered a force press is no longer in contact. |
| **`on_hover`** | `HoverEvent` | Called when a mouse pointer has entered this control (updates coordinates). |
| **`on_enter`** | `HoverEvent` | Called when a mouse pointer has entered this control. |
| **`on_exit`** | `HoverEvent` | Called when a mouse pointer has exited this control. |
| **`on_scale_start`** | `ScaleStartEvent` | Called when pointers establish a focal point and initial scale of 1.0. |
| **`on_scale_update`** | `ScaleUpdateEvent` | TBD |
| **`on_scale_end`** | `ScaleEndEvent` | TBD |
| **`on_scroll`** | `ScrollEvent` | TBD |