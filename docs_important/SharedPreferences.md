# SharedPreferences

Provides access to persistent key-value storage.

**Inherits:** `Service`

---

## Methods Summary

* **`clear`**: Clears all keys and values.
* **`contains_key`**: Checks if the given key exists.
* **`get`**: Gets the value for the given key.
* **`get_keys`**: Gets all keys with the given prefix.
* **`remove`**: Removes the value for the given key.
* **`set`**: Sets a value for the given key.

---

## Examples

### Basic Example

```python
import flet as ft

async def main(page: ft.Page):
    
    async def set_value(e):
        # Note: Added 'e' argument to handle the event correctly
        await ft.SharedPreferences().set(store_key.value, store_value.value)
        # Update the 'get' field to match what we just set
        get_key.value = store_key.value
        store_key.value = ""
        store_value.value = ""
        page.show_dialog(ft.SnackBar(ft.Text("Value saved to SharedPreferences")))

    async def get_value(e):
        contents = await ft.SharedPreferences().get(get_key.value)
        page.add(ft.Text(f"SharedPreferences contents: {contents}"))

    page.add(
        ft.Column(
            [
                ft.Row(
                    [
                        store_key := ft.TextField(label="Key"),
                        store_value := ft.TextField(label="Value"),
                        ft.Button("Set", on_click=set_value),
                    ]
                ),
                ft.Row(
                    [
                        get_key := ft.TextField(label="Key"),
                        ft.Button("Get", on_click=get_value),
                    ]
                ),
            ],
        )
    )

ft.run(main)

```

---

## API Reference

### Methods

#### `clear` (Async)

```python
clear() -> bool

```

Clears all keys and values.

#### `contains_key` (Async)

```python
contains_key(key: str) -> bool

```

Checks if the given key exists.

* **Parameters:**
* `key` (str): The key to search for.


* **Returns:** `bool` - True if the key exists, False otherwise.

#### `get` (Async)

```python
get(key: str)

```

Gets the value for the given key.

* **Parameters:**
* `key` (str): The key to retrieve the value for.



#### `get_keys` (Async)

```python
get_keys(key_prefix: str) -> list[str]

```

Gets all keys with the given prefix.

* **Parameters:**
* `key_prefix` (str): The prefix to filter keys by.


* **Returns:** `list[str]` - A list of keys matching the prefix.

#### `remove` (Async)

```python
remove(key: str) -> bool

```

Removes the value for the given key.

* **Parameters:**
* `key` (str): The key to remove.


* **Returns:** `bool` - True if the removal was successful.

#### `set` (Async)

```python
set(key: str, value: Any) -> bool

```

Sets a value for the given key.

* **Parameters:**
* `key` (str): The key to set.
* `value` (Any): The value to store.


* **Returns:** `bool` - True if the operation was successful.