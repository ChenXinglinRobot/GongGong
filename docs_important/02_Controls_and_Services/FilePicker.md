# FilePicker

A control that allows you to use the native file explorer to pick single or multiple files, with extensions filtering support and upload capabilities.

> **Important:** On Linux, this control requires **Zenity** when running Flet as a desktop app. It is not required when running Flet in a browser.
> To install Zenity on Ubuntu/Debian run:
> ```bash
> sudo apt-get install zenity
> 
> ```
> 
> 

**Inherits:** `Service`

---

## Events

* **`on_upload(EventHandler[FilePickerUploadEvent] | None)`**
Called when a file is uploaded via the `upload()` method.

## Methods Summary

* **`get_directory_path`**: Selects a directory and returns its absolute path.
* **`pick_files`**: Opens a pick file dialog.
* **`save_file`**: Opens a save file dialog which lets the user select a file path and a file name to save a file.
* **`upload`**: Uploads picked files to specified upload URLs.

---

## Usage

Create an instance of `FilePicker`:

```python
import flet as ft

file_picker = ft.FilePicker()

```

To open the file picker dialog, call one of these three methods depending on the use case: `pick_files()`, `save_file()`, or `get_directory_path()`.

In most cases, you can use a lambda function attached to a button:

```python
ft.Button(
    content="Pick files",
    on_click=lambda _: file_picker.pick_files(allow_multiple=True)
)

```

### Uploading Files

To upload one or more files, the process involves two steps:

1. Call `FilePicker.pick_files()` to let the user select files.
2. Pass the returned list to `FilePicker.upload()` to perform the upload.

#### Separate uploads per user

If you need to separate uploads for each user, you can specify a filename prepended with any number of directories in the `page.get_upload_url()` call.

Example:

```python
upload_url = page.get_upload_url(f"/{username}/pictures/{f.name}", 600)

```

*Note: `/{username}/pictures` directories will be automatically created inside `upload_dir` if they do not exist.*

### Upload Storage

The `page.get_upload_url()` method generates a presigned upload URL for Flet's internal upload storage.

**Use any storage for file uploads**
You can generate a presigned upload URL for AWS S3 storage using the `boto3` library. The same technique works for **Wasabi**, **Backblaze**, **MinIO**, and any other storage providers with an S3-compatible API.

To enable Flet to save uploaded files to a specific directory, provide a full or relative path in the `flet.run()` call:

```python
ft.run(main, upload_dir="uploads")

```

You can also place uploads inside the `assets` directory, allowing files (e.g., pictures, docs) to be accessed by the Flet client immediately:

```python
ft.run(main, assets_dir="assets", upload_dir="assets/uploads")

```

In your app, you can then display the uploaded picture using:

```python
ft.Image(src="/uploads/<some-uploaded-picture.png>")

```

---

## Examples

### 1. Pick, Save, and Get Directory Paths

```python
import flet as ft

def main(page: ft.Page):
    async def handle_pick_files(e: ft.Event[ft.Button]):
        files = await ft.FilePicker().pick_files(allow_multiple=True)
        selected_files.value = (
            ", ".join(map(lambda f: f.name, files)) if files else "Cancelled!"
        )

    async def handle_save_file(e: ft.Event[ft.Button]):
        save_file_path.value = await ft.FilePicker().save_file()

    async def handle_get_directory_path(e: ft.Event[ft.Button]):
        directory_path.value = await ft.FilePicker().get_directory_path()

    page.add(
        ft.Row(
            controls=[
                ft.Button(
                    content="Pick files",
                    icon=ft.Icons.UPLOAD_FILE,
                    on_click=handle_pick_files,
                ),
                selected_files := ft.Text(),
            ]
        ),
        ft.Row(
            controls=[
                ft.Button(
                    content="Save file",
                    icon=ft.Icons.SAVE,
                    on_click=handle_save_file,
                    disabled=page.web,  # disable this button in web mode
                ),
                save_file_path := ft.Text(),
            ]
        ),
        ft.Row(
            controls=[
                ft.Button(
                    content="Open directory",
                    icon=ft.Icons.FOLDER_OPEN,
                    on_click=handle_get_directory_path,
                    disabled=page.web,  # disable this button in web mode
                ),
                directory_path := ft.Text(),
            ]
        ),
    )

ft.run(main)

```

### 2. Pick and Upload Files

The following example demonstrates a multi-file pick and upload app with progress indication.

> **Note:** To run this example locally for web testing:
> 1. Export a secret key: `export FLET_SECRET_KEY=<some_secret_key>`
> 2. Run: `uv run flet run --web examples/services/file_picker/pick_and_upload.py`
> 
> 

```python
from dataclasses import dataclass, field
import flet as ft

@dataclass
class State:
    file_picker: ft.FilePicker | None = None
    picked_files: list[ft.FilePickerFile] = field(default_factory=list)

state = State()

def main(page: ft.Page):
    if not page.web:
        page.add(
            ft.Text(
                "This example is only available in Flet Web mode.",
                color=ft.Colors.RED,
                selectable=True,
            )
        )
        return

    prog_bars: dict[str, ft.ProgressRing] = {}

    def on_upload_progress(e: ft.FilePickerUploadEvent):
        prog_bars[e.file_name].value = e.progress

    async def handle_files_pick(e: ft.Event[ft.Button]):
        state.file_picker = ft.FilePicker(on_upload=on_upload_progress)
        files = await state.file_picker.pick_files(allow_multiple=True)
        print("Picked files:", files)
        state.picked_files = files

        # update progress bars
        upload_button.disabled = len(files) == 0
        prog_bars.clear()
        upload_progress.controls.clear()
        for f in files:
            prog = ft.ProgressRing(value=0, bgcolor="#eeeeee", width=20, height=20)
            prog_bars[f.name] = prog
            upload_progress.controls.append(ft.Row([prog, ft.Text(f.name)]))

    async def handle_file_upload(e: ft.Event[ft.Button]):
        upload_button.disabled = True
        await state.file_picker.upload(
            files=[
                ft.FilePickerUploadFile(
                    name=file.name,
                    upload_url=page.get_upload_url(f"dir/{file.name}", 60),
                )
                for file in state.picked_files
            ]
        )

    page.add(
        ft.Button(
            content="Select files...",
            icon=ft.Icons.FOLDER_OPEN,
            on_click=handle_files_pick,
        ),
        upload_progress := ft.Column(),
        upload_button := ft.Button(
            content="Upload",
            icon=ft.Icons.UPLOAD,
            on_click=handle_file_upload,
            disabled=True,
        ),
    )

ft.run(main, upload_dir="examples")

```

---

## API Reference

### Events

#### `on_upload`

`EventHandler[FilePickerUploadEvent] | None`

Called when a file is uploaded via the `upload()` method.
This callback is invoked at least twice for each uploaded file:

1. Once with `0.0` progress before the upload starts.
2. Once with `1.0` progress when the upload completes.

For files larger than 1 MB, additional progress events are emitted at every 10% increment (e.g., `0.1`, `0.2`, ...).

### Methods

#### `get_directory_path` (Async)

```python
get_directory_path(
    dialog_title: str | None = None,
    initial_directory: str | None = None,
) -> str | None

```

Selects a directory and returns its absolute path.

* **Parameters:**
* `dialog_title` (str | None): The title of the dialog window.
* `initial_directory` (str | None): The initial directory where the dialog should open.


* **Returns:** `str | None` - The selected directory path or `None` if cancelled.
* **Raises:** `FletUnsupportedPlatformException` if called in web mode.

#### `pick_files` (Async)

```python
pick_files(
    dialog_title: str | None = None,
    initial_directory: str | None = None,
    file_type: FilePickerFileType = ANY,
    allowed_extensions: list[str] | None = None,
    allow_multiple: bool = False,
) -> list[FilePickerFile]

```

Opens a pick file dialog.
*Tip: To upload the picked files, pass them to the `upload()` method along with their upload URLs.*

* **Parameters:**
* `dialog_title` (str | None): The title of the dialog window.
* `initial_directory` (str | None): The initial directory where the dialog should open.
* `file_type` (FilePickerFileType): The file types allowed (Default: `ANY`).
* `allow_multiple` (bool): Allow selection of multiple files (Default: `False`).
* `allowed_extensions` (list[str] | None): Allowed file extensions. Only effective if `file_type` is `FilePickerFileType.CUSTOM`.


* **Returns:** `list[FilePickerFile]` - A list of selected files.

#### `save_file` (Async)

```python
save_file(
    dialog_title: str | None = None,
    file_name: str | None = None,
    initial_directory: str | None = None,
    file_type: FilePickerFileType = ANY,
    allowed_extensions: list[str] | None = None,
    src_bytes: bytes | None = None,
) -> str | None

```

Opens a save file dialog letting the user select a file path and name.

> **Note:** On desktop, this method only opens a dialog for the user to select a location and file name, and returns the chosen path. The file itself is not created or saved by this method alone.

* **Parameters:**
* `dialog_title` (str | None): The title of the dialog window.
* `file_name` (str | None): The default file name.
* `initial_directory` (str | None): Initial directory.
* `file_type` (FilePickerFileType): Allowed file types.
* `src_bytes` (bytes | None): The contents of the file. **Must be provided in web, iOS, or Android modes.**
* `allowed_extensions` (list[str] | None): Allowed extensions if `file_type` is `CUSTOM`.


* **Raises:**
* `ValueError`: If `src_bytes` is not provided in web, iOS, or Android modes.
* `ValueError`: If `file_name` is not provided in web mode.



#### `upload` (Async)

```python
upload(files: list[FilePickerUploadFile])

```

Uploads picked files to specified upload URLs.

* Before calling this, `pick_files()` must be called to ensure internal selection is not empty.
* Flet asynchronously uploads files one-by-one and reports progress via `on_upload`.
* **Parameters:**
* `files` (list[FilePickerUploadFile]): A list specifying which files to upload and where (via PUT or POST).