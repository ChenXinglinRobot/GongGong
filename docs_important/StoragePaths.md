# StoragePaths

Provides access to commonly used storage paths on the device.

> **Note:** Its methods are not supported in web mode.

**Inherits:** `Service`

---

## Methods Summary

* **`get_application_cache_directory`**: Returns the path to the application-specific cache directory.
* **`get_application_documents_directory`**: Returns the path to a directory for user-generated data.
* **`get_application_support_directory`**: Returns the path to a directory for application support files.
* **`get_console_log_filename`**: Returns the path to a `console.log` file for debugging.
* **`get_downloads_directory`**: Returns the path to the downloads directory.
* **`get_external_cache_directories`**: Returns paths to external cache directories.
* **`get_external_storage_directories`**: Returns paths to external storage directories.
* **`get_external_storage_directory`**: Returns the path to the top-level external storage directory.
* **`get_library_directory`**: Returns the path to the library directory.
* **`get_temporary_directory`**: Returns the path to the temporary directory.

---

## Examples

### Basic Example

```python
import flet as ft

async def main(page: ft.Page):
    storage_paths = ft.StoragePaths()

    items = []
    for label, method in [
        ("Application cache directory", storage_paths.get_application_cache_directory),
        (
            "Application documents directory",
            storage_paths.get_application_documents_directory,
        ),
        (
            "Application support directory",
            storage_paths.get_application_support_directory,
        ),
        ("Downloads directory", storage_paths.get_downloads_directory),
        ("External cache directories", storage_paths.get_external_cache_directories),
        (
            "External storage directories",
            storage_paths.get_external_storage_directories,
        ),
        ("Library directory", storage_paths.get_library_directory),
        ("External storage directory", storage_paths.get_external_storage_directory),
        ("Temporary directory", storage_paths.get_temporary_directory),
        ("Console log filename", storage_paths.get_console_log_filename),
    ]:
        try:
            value = await method()
        except ft.FletUnsupportedPlatformException as e:
            value = f"Not supported: {e}"
        except Exception as e:
            value = f"Error: {e}"
        else:
            if isinstance(value, list):
                value = ", ".join(value)
            elif value is None:
                value = "Unavailable"

        items.append(
            ft.Text(
                spans=[
                    ft.TextSpan(
                        f"{label}: ", style=ft.TextStyle(weight=ft.FontWeight.BOLD)
                    ),
                    ft.TextSpan(value),
                ]
            )
        )

    page.add(ft.Column(items, spacing=5))

ft.run(main)

```

---

## API Reference

### Methods

#### `get_application_cache_directory` (Async)

```python
get_application_cache_directory() -> str

```

Returns the path to the application-specific cache directory. If this directory does not exist, it is created automatically.

* **Returns:** `str` - The path to a directory where the application may place cache files.
* **Raises:** `FletUnsupportedPlatformException` if called on the web platform.

#### `get_application_documents_directory` (Async)

```python
get_application_documents_directory() -> str

```

Returns the path to a directory for user-generated data. This directory is intended for data that cannot be recreated by your application.

For non-user-generated data, consider using:

* `get_application_support_directory()`
* `get_application_cache_directory()`
* `get_external_storage_directory()`
* **Returns:** `str` - The path to the application documents directory.
* **Raises:** `FletUnsupportedPlatformException` if called on the web platform.

#### `get_application_support_directory` (Async)

```python
get_application_support_directory() -> str

```

Returns the path to a directory for application support files. This directory is created automatically if it does not exist. Use this for files not exposed to the user. Do not use for user data files.

* **Returns:** `str` - The path to the application support directory.
* **Raises:** `FletUnsupportedPlatformException` if called on the web platform.

#### `get_console_log_filename` (Async)

```python
get_console_log_filename() -> str

```

Returns the path to a `console.log` file for debugging. This file is located in the application cache directory.

* **Returns:** `str` - The path to the console log file.
* **Raises:** `FletUnsupportedPlatformException` if called on the web platform.

#### `get_downloads_directory` (Async)

```python
get_downloads_directory() -> str | None

```

Returns the path to the downloads directory. The returned directory may not exist; clients should verify and create it if necessary.

* **Returns:** `str | None` - The path to the downloads directory, or `None` if unavailable.
* **Raises:** `FletUnsupportedPlatformException` if called on the web platform.

#### `get_external_cache_directories` (Async)

```python
get_external_cache_directories() -> list[str] | None

```

Returns paths to external cache directories. These directories are typically on external storage (e.g., SD cards). Multiple directories may be available on some devices.

* **Returns:** `list[str] | None` - A list of external cache directory paths, or `None` if unavailable.
* **Raises:** `FletUnsupportedPlatformException` if called on the web or non-Android platforms.

#### `get_external_storage_directories` (Async)

```python
get_external_storage_directories() -> list[str] | None

```

Returns paths to external storage directories. These directories are typically on external storage (e.g., SD cards). Multiple directories may be available on some devices.

* **Returns:** `list[str] | None` - A list of external storage directory paths, or `None` if unavailable.
* **Raises:** `FletUnsupportedPlatformException` if called on the web or non-Android platforms.

#### `get_external_storage_directory` (Async)

```python
get_external_storage_directory() -> str | None

```

Returns the path to the top-level external storage directory.

* **Returns:** `str | None` - The path to the external storage directory, or `None` if unavailable.
* **Raises:** `FletUnsupportedPlatformException` if called on the web or non-Android platforms.

#### `get_library_directory` (Async)

```python
get_library_directory() -> str

```

Returns the path to the library directory. This directory is for persistent, backed-up files not visible to the user (e.g., `sqlite.db`).

* **Returns:** `str` - The path to the library directory.
* **Raises:** `FletUnsupportedPlatformException` if called on the web or non-Apple platforms.

#### `get_temporary_directory` (Async)

```python
get_temporary_directory() -> str

```

Returns the path to the temporary directory. This directory is not backed up and is suitable for storing caches of downloaded files. Files may be cleared at any time. The caller is responsible for managing files within this directory.

* **Returns:** `str` - The path to the temporary directory.
* **Raises:** `FletUnsupportedPlatformException` if called on the web platform.