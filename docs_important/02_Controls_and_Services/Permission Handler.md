# Permission Handler

Manage runtime permissions in your Flet apps using the `flet-permission-handler` extension, powered by Flutter's `permission_handler`.

**Inherits:** `Service`

---

## Platform Support

| Platform | Supported |
| --- | --- |
| Windows | ✅ |
| macOS | ❌ |
| Linux | ❌ |
| iOS | ✅ |
| Android | ✅ |
| Web | ✅ |

---

## Usage

Add `flet-permission-handler` to your project dependencies:

```bash
uv add flet-permission-handler

```

*Or using pip:*

```bash
pip install flet-permission-handler

```

> **Note:** On mobile platforms (Android/iOS), you must also declare permissions in the native project files (e.g., `AndroidManifest.xml` or `Info.plist`). See **Flet publish docs** for details on how to configure these.

### Example

```python
import flet as ft
import flet_permission_handler as fph

def main(page: ft.Page):
    page.appbar = ft.AppBar(title="PermissionHandler Playground")
    
    ph = fph.PermissionHandler()

    def show_snackbar(message: str):
        page.show_dialog(ft.SnackBar(ft.Text(message)))

    async def get_permission_status(e: ft.Event):
        # Check current status of microphone
        status = await ph.get_status(fph.Permission.MICROPHONE)
        show_snackbar(f"Microphone permission status: {status.name}")

    async def request_permission(e: ft.Event):
        # Request access to microphone
        status = await ph.request(fph.Permission.MICROPHONE)
        show_snackbar(f"Requested microphone permission: {status.name}")

    async def open_app_settings(e: ft.Event):
        show_snackbar("Opening app settings...")
        await ph.open_app_settings()

    page.add(
        ft.OutlinedButton("Open app settings", on_click=open_app_settings),
        ft.OutlinedButton("Request Microphone permission", on_click=request_permission),
        ft.OutlinedButton(
            "Get Microphone permission status", on_click=get_permission_status
        ),
    )

ft.run(main)

```

---

## API Reference

**Description:** Manages permissions for the application.

**Raises:**

* `FletUnsupportedPlatformException`: If the platform is not supported (currently supports Android, iOS, Windows, and Web).

### Methods

#### `get_status` (Async)

```python
get_status(permission: Permission) -> PermissionStatus | None

```

Gets the current status of the given permission.

* **Parameters:**
* `permission` (Permission): The `Permission` enum to check the status for.


* **Returns:** `PermissionStatus | None` - A `PermissionStatus` if the status is known, otherwise `None`.

#### `open_app_settings` (Async)

```python
open_app_settings() -> bool

```

Opens the device's app settings page.

* **Returns:** `bool` - `True` if the app settings page could be opened, otherwise `False`.

#### `request` (Async)

```python
request(permission: Permission) -> PermissionStatus | None

```

Requests the user for access to the specific permission if access hasn't already been granted.

* **Parameters:**
* `permission` (Permission): The `Permission` enum to request.


* **Returns:** `PermissionStatus | None` - The new `PermissionStatus` after the request, or `None` if the request was not successful.