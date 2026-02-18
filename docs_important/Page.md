这是一个基于你提供的文档内容整理的Markdown格式文档，详细介绍了 `Page` 类的属性、事件、方法及使用示例。

---

# Page

`Page` is a container for `View` controls. A page instance and the root view are automatically created when a new user session starts.

**Inherits:** `BasePage`

## Properties

| Property | Type | Read-Only | Description |
| --- | --- | --- | --- |
| **`auth`** | `Optional[Authorization]` |  | The current authorization context, or `None` if the user is not authorized. |
| **`browser_context_menu`** | - |  | **DEPRECATED**: The BrowserContextMenu service for the current page. |
| **`client_ip`** | `Optional[str]` | ✅ | IP address of the connected user. (Web only). |
| **`client_user_agent`** | `Optional[str]` | ✅ | Browser details of the connected user. (Web only). |
| **`clipboard`** | - |  | **DEPRECATED**: The Clipboard service for the current page. |
| **`debug`** | `bool` | ✅ | `True` if Flutter client of Flet app is running in debug mode. |
| **`executor`** | `Optional[ThreadPoolExecutor]` |  | The executor for the current page. |
| **`fonts`** | `Optional[dict[str, str]]` |  | Defines custom fonts. Key is family name, Value is URL/path to `.ttc`, `.ttf`, or `.otf`. |
| **`loop`** | `AbstractEventLoop` |  | The event loop for the current page. |
| **`multi_view`** | `bool` | ✅ | `True` if the application is running with multi-view support. |
| **`multi_views`** | `list[MultiView]` |  | The list of multi-views associated with this page. |
| **`name`** | `str` |  | The name of the current page. |
| **`platform`** | `Optional[PagePlatform]` |  | The operating system the application is running on. |
| **`platform_brightness`** | `Optional[Brightness]` | ✅ | The current brightness mode of the host platform. |
| **`pubsub`** | `PubSubClient` |  | The PubSub client for the current page. |
| **`pwa`** | `bool` | ✅ | `True` if the application is running as Progressive Web App (PWA). |
| **`pyodide`** | `bool` | ✅ | `True` if the application is running in Pyodide (WebAssembly) mode. |
| **`query`** | `QueryString` |  | The query parameters of the current page. |
| **`route`** | `str` | ✅ | Gets current app route. Default is `/`. |
| **`session`** | `Session` |  | The session that this page belongs to. |
| **`shared_preferences`** | - |  | **DEPRECATED**: The SharedPreferences service for the current page. |
| **`storage_paths`** | - |  | **DEPRECATED**: The StoragePaths service for the current page. |
| **`test`** | `bool` | ✅ | `True` if the application is running with test mode. |
| **`url`** | `Optional[str]` |  | The URL of the current page. |
| **`url_launcher`** | - |  | **DEPRECATED**: The UrlLauncher service for the current page. |
| **`wasm`** | `bool` | ✅ | `True` if the application is running in WebAssembly (WASM) mode. |
| **`web`** | `bool` | ✅ | `True` if the application is running in the web browser. |
| **`window`** | `Window` |  | Provides properties/methods/events to monitor and control the app's native OS window. |

---

## Events

| Event | Type | Description |
| --- | --- | --- |
| **`on_app_lifecycle_state_change`** | `EventHandler` | Triggers when app lifecycle state changes. |
| **`on_close`** | `ControlEventHandler` | Called when a session has expired after configured amount of time (60 minutes by default). |
| **`on_connect`** | `ControlEventHandler` | Called when a web user (re-)connects to a page session (e.g., refresh, unlock). |
| **`on_disconnect`** | `ControlEventHandler` | Called when a web user disconnects (closes tab/window). |
| **`on_error`** | `ControlEventHandler` | Called when unhandled exception occurs. |
| **`on_keyboard_event`** | `EventHandler` | Called when a keyboard key is pressed. |
| **`on_login`** | `EventHandler` | Called upon successful or failed OAuth authorization flow. |
| **`on_logout`** | `ControlEventHandler` | Called after `page.logout()` call. |
| **`on_multi_view_add`** | `EventHandler` | TBD |
| **`on_multi_view_remove`** | `EventHandler` | TBD |
| **`on_platform_brightness_change`** | `EventHandler` | Called when brightness of app host platform has changed. |
| **`on_route_change`** | `EventHandler` | Called when page route changes (programmatically or via URL/Back button). |
| **`on_view_pop`** | `EventHandler` | Called when the user clicks automatic "Back" button in `AppBar`. |

---

## Methods

### `can_launch_url`

```python
async can_launch_url(url: str) -> bool

```

Checks whether the specified URL can be handled by some app installed on the device.

* **Returns:** `False` on Web (mostly) and recent Android/iOS versions unless configured.

### `close_in_app_web_view`

```python
async close_in_app_web_view() -> None

```

Closes in-app web view opened with `launch_url()`. (Mobile only).

### `get_control`

```python
get_control(id: int) -> Optional[BaseControl]

```

Get a control by its ID.

### `get_device_info`

```python
async get_device_info() -> Optional[DeviceInfo]

```

Returns device information object for the current platform.

### `get_upload_url`

```python
get_upload_url(file_name: str, expires: int) -> str

```

Generates presigned upload URL for built-in upload storage.

* Requires `upload_dir` argument in `ft.run()`.

### `go`

```python
go(route: str, skip_route_change_event: bool = False, **kwargs: Any) -> None

```

A helper method that updates `page.route`, calls `page.on_route_change`, and finally calls `page.update()`.

### `launch_url`

```python
async launch_url(url: Union[str, Url], ...) -> None

```

Opens a web browser or popup window to a given URL.

* **Parameters:**
* `web_popup_window_name`: `UrlTarget.SELF`, `UrlTarget.BLANK`, or custom name.



### `login`

```python
async login(provider: OAuthProvider, ...) -> AT

```

Starts OAuth flow.

### `logout`

```python
logout() -> None

```

Clears current authentication context.

### `push_route`

```python
async push_route(route: str, **kwargs: Any) -> None

```

Pushes a new navigation route to the browser history stack. Fires `on_route_change`.

### `run_task`

```python
run_task(handler: Callable, *args, **kwargs) -> Future

```

Run handler coroutine as a new Task in the event loop associated with the current page.

### `run_thread`

```python
run_thread(handler: Callable, *args, **kwargs) -> None

```

Run handler function as a new Thread in the executor associated with the current page.

### `set_allowed_device_orientations`

```python
async set_allowed_device_orientations(orientations: list[DeviceOrientation]) -> None

```

Constrains the allowed orientations for the app when running on a mobile device.

* **Limitations:**
* **Android 16+:** Cannot change orientation if display width ≥ 600 dp.
* **iOS:** Only works on iPad if multitasking is disabled.



### `update`

```python
update(*controls) -> None

```

Updates the page or specific controls.

---

## Examples

### Listening to Keyboard Events

```python
import flet as ft

class ButtonControl(ft.Container):
    def __init__(self, text):
        super().__init__()
        self.content: ft.Text = ft.Text(text)
        self.border = ft.Border.all(1, ft.Colors.BLACK_54)
        self.border_radius = 3
        self.bgcolor = "0x09000000"
        self.padding = 10
        self.visible = False

def main(page: ft.Page):
    page.spacing = 50
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def on_keyboard(e: ft.KeyboardEvent):
        key.content.value = e.key
        key.visible = True
        shift.visible = e.shift
        ctrl.visible = e.ctrl
        alt.visible = e.alt
        meta.visible = e.meta
        page.update()

    page.on_keyboard_event = on_keyboard

    page.add(
        ft.Text("Press any key with a combination of CTRL, ALT, SHIFT and META keys..."),
        ft.Row(
            controls=[
                key := ButtonControl(""),
                shift := ButtonControl("Shift"),
                ctrl := ButtonControl("Control"),
                alt := ButtonControl("Alt"),
                meta := ButtonControl("Meta"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        ),
    )

ft.run(main)

```

### Mobile Device Orientation Configuration

```python
import flet as ft

def main(page: ft.Page) -> None:
    page.title = "Device orientation lock"
    page.appbar = ft.AppBar(title=ft.Text("Device orientation Playground"), center_title=True, bgcolor=ft.Colors.BLUE)

    def handle_media_change(e: ft.PageMediaData) -> None:
        page.show_dialog(
            ft.SnackBar(
                f"I see you rotated the device to {e.orientation.name} orientation. 👀",
                action="Haha!",
                duration=ft.Duration(seconds=3),
            )
        )

    page.on_media_change = handle_media_change

    async def on_checkbox_change(e: ft.Event[ft.Checkbox]) -> None:
        selected = [o for o, checkbox in checkboxes.items() if checkbox.value]
        await page.set_allowed_device_orientations(selected)

    checkboxes: dict[ft.DeviceOrientation, ft.Checkbox] = {
        orientation: ft.Checkbox(
            label=orientation.name,
            value=True,
            on_change=on_checkbox_change,
            disabled=not page.platform.is_mobile(),
        )
        for orientation in list(ft.DeviceOrientation)
    }

    page.add(
        ft.Text(spans=[
            ft.TextSpan("Select enabled orientations.", visible=page.platform.is_mobile()),
            ft.TextSpan("Open on mobile device.", visible=not page.platform.is_mobile(), style=ft.TextStyle(weight=ft.FontWeight.BOLD)),
        ]),
        ft.Column(controls=list(checkboxes.values())),
    )

if __name__ == "__main__":
    ft.run(main)

```

### App Exit Confirmation

```python
import flet as ft

def main(page: ft.Page):
    def window_event(e: ft.WindowEvent):
        if e.type == ft.WindowEventType.CLOSE:
            page.show_dialog(confirm_dialog)
            page.update()

    page.window.prevent_close = True
    page.window.on_event = window_event

    async def handle_yes_click(e: ft.Event[ft.Button]):
        await page.window.destroy()

    def handle_no_click(e: ft.Event[ft.OutlinedButton]):
        page.pop_dialog()
        page.update()

    confirm_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("Please confirm"),
        content=ft.Text("Do you really want to exit this app?"),
        actions=[
            ft.Button(content="Yes", on_click=handle_yes_click),
            ft.OutlinedButton(content="No", on_click=handle_no_click),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    page.add(ft.Text('Try exiting this app by clicking window\'s "Close" button!'))

ft.run(main)

```

### Hidden App Window on Startup

```python
import asyncio
import flet as ft

async def main(page: ft.Page):
    print("Window is hidden on start. Will show after 3 seconds...")
    page.add(ft.Text("Hello!"))
    page.window.width = 300
    page.window.height = 200
    page.update()
    await page.window.center()
    await asyncio.sleep(3)
    page.window.visible = True
    page.update()

# Run with -n or --hidden flag usually, or use view=ft.AppView.FLET_APP_HIDDEN
ft.run(main, view=ft.AppView.FLET_APP_HIDDEN)

```

### Toggle Semantics Debugger

```python
import flet as ft

def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def on_keyboard(e: ft.KeyboardEvent):
        if e.shift and e.key == "S":
            page.show_semantics_debugger = not page.show_semantics_debugger
            page.update()

    page.on_keyboard_event = on_keyboard

    def button_click(e: ft.Event[ft.Button]):
        counter.value = str(int(counter.value) + 1)
        page.update()

    page.add(
        counter := ft.Text("0", size=40),
        ft.Text("Press Shift+S to toggle semantics debugger"),
        ft.Button(content="Increment number", icon=ft.Icons.ADD, on_click=button_click),
    )

ft.run(main)

```