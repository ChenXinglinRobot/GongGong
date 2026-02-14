# Read and Write Files

In some cases, you need to read and write files to disk. For example, you might need to persist data across app launches, or download data from the internet and save it for later offline use.

Flet makes it easy to work with files and directories on the mobile/desktop device using standard Python file operations.

---

## Storage Paths

Flet provides two directory paths for data storage, available as environment variables:

* **`FLET_APP_STORAGE_DATA`**: Path for persistent application data.
* **`FLET_APP_STORAGE_TEMP`**: Path for temporary data.

You can access their values using the `os` module:

```python
import os

app_data_path = os.getenv("FLET_APP_STORAGE_DATA")
app_temp_path = os.getenv("FLET_APP_STORAGE_TEMP")

```

---

## Basic Operations

### Writing to a File

To write data to a new or existing file, you can use the built-in `open` function combined with the path variables.

```python
import os

app_data_path = os.getenv("FLET_APP_STORAGE_DATA")
# Construct the full file path
my_file_path = os.path.join(app_data_path, "test_file.txt")

with open(my_file_path, "w") as f:
    f.write("Some file content...")

```

### Reading from a File

To read data from an existing file:

```python
import os

app_data_path = os.getenv("FLET_APP_STORAGE_DATA")
my_file_path = os.path.join(app_data_path, "test_file.txt")

with open(my_file_path, "r") as f:
    file_content = f.read()
    print(file_content)

```

> **Note:** You can use the `os` module (or any other standard library tool) to perform various file operations like renaming, deleting, or listing files present in the directory.

---

## Example: Counter App

Below is an example of a basic Counter application where the value persists across app launches. This is achieved by writing the counter value to a file in the app's data storage directory and reading it when the app launches.

This example also utilizes **`FLET_APP_CONSOLE`**, an environment variable that points to the application's `console.log` file, allowing you to view `print()` statements in production mode.

```python
import os
from datetime import datetime
import flet as ft

# constants
FLET_APP_STORAGE_DATA = os.getenv("FLET_APP_STORAGE_DATA")
COUNTER_FILE_PATH = os.path.join(FLET_APP_STORAGE_DATA, "counter.txt")
FLET_APP_CONSOLE = os.getenv("FLET_APP_CONSOLE")


class Counter(ft.Text):
    def __init__(self, storage_path=COUNTER_FILE_PATH):
        super().__init__(theme_style=ft.TextThemeStyle.HEADLINE_LARGE)
        self.storage_path = storage_path
        self.count = self.__read_from_storage()

    def increment(self):
        """Increment the counter, store the new value, and return it."""
        self.count += 1
        self.update()
        self.__write_to_storage()

    def before_update(self):
        super().before_update()
        self.value = f"Button tapped {self.count} time{'' if self.count == 1 else 's'}"

    def __log(self, action: str, value: int = None):
        """Log executed action."""
        if value is None:
            value = self.count
        print(f"{datetime.now().strftime('%Y/%m/%d %H:%M:%S')} - {action} = {value}")

    def __read_from_storage(self):
        """Read counter value. If an error occurs, use 0."""
        try:
            with open(self.storage_path, "r") as f:
                value = int(f.read().strip())
        except (FileNotFoundError, ValueError):
            # file does not exist or int parsing failed
            value = 0

        self.__log("READ", value)
        return value

    def __write_to_storage(self):
        """Write current counter value to storage."""
        with open(self.storage_path, "w") as f:
            f.write(str(self.count))
        self.__log("WRITE")


def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def show_logs(e: ft.ControlEvent):
        if FLET_APP_CONSOLE is not None:
            with open(FLET_APP_CONSOLE, "r") as f:
                dlg = ft.AlertDialog(
                    title=ft.Text("App Logs"),
                    content=ft.Text(f.read()),
                    scrollable=True,
                )
                page.open(dlg)

    counter = Counter()
    page.appbar = ft.AppBar(
        title=ft.Text("Storage Playground", weight=ft.FontWeight.BOLD),
        center_title=True,
        bgcolor=ft.Colors.BLUE,
        color=ft.Colors.WHITE,
        adaptive=True,
        actions=[
            ft.IconButton(
                icon=ft.Icons.REMOVE_RED_EYE,
                tooltip="Show logs",
                visible=FLET_APP_CONSOLE is not None,
                on_click=show_logs,
            ),
        ],
    )
    page.floating_action_button = ft.FloatingActionButton(
        icon=ft.Icons.ADD,
        text="Increment Counter",
        foreground_color=ft.Colors.WHITE,
        bgcolor=ft.Colors.BLUE,
        on_click=lambda e: counter.increment(),
    )
    page.floating_action_button_location = ft.FloatingActionButtonLocation.CENTER_FLOAT

    page.add(ft.SafeArea(counter))


ft.run(main)

```