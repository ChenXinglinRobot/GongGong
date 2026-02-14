# Client Storage

Flet's client storage API allows storing key-value data on the client side in persistent storage. The Flet implementation uses the `shared_preferences` Flutter package.

The actual storage mechanism depends on the platform where the Flet app is running:

* **Web:** Local storage.
* **Desktop:** JSON file.
* **iOS:** NSUserDefaults.
* **Android:** SharedPreferences.

---

## Usage

### Writing Data

You can store various data types including strings, numbers, booleans, and lists.

```python
# strings
await page.shared_preferences.set("key", "value")

# numbers, booleans
await page.shared_preferences.set("number.setting", 12345)
await page.shared_preferences.set("bool_setting", True)

# lists
await page.shared_preferences.set("favorite_colors", ["red", "green", "blue"])

```

> **Note:** Each Flutter application using the `shared_preferences` plugin has its own set of preferences. However, since the same Flet client (which is a Flutter app) is used to run the UI for multiple Flet apps, **any values stored in one Flet application are visible/available to another Flet app running by the same user.**
> To distinguish one application's settings from another, it is recommended to use a unique prefix for all storage keys, for example `{company}.{product}.`.
> * App 1: `acme.one_app.auth_token`
> * App 2: `acme.second_app.auth_token`
> 
> 

> **Caution:** It is the responsibility of the Flet app developer to **encrypt sensitive data** before sending it to client storage, so it cannot be read or tampered with by another app or an app user.

### Reading Data

Values are automatically converted back to their original type upon retrieval.

```python
# The value is automatically converted back to the original type
value = await page.shared_preferences.get("key")

colors = await page.shared_preferences.get("favorite_colors")
# colors = ["red", "green", "blue"]

```

### Checking Keys

Check if a specific key exists in storage:

```python
exists = await page.shared_preferences.contains_key("key") 
# Returns True if the key exists

```

### Get All Keys

Retrieve all keys, optionally filtering by a prefix:

```python
keys = await page.shared_preferences.get_keys("key-prefix.")

```

### Removing Data

Remove a single value by its key:

```python
await page.shared_preferences.remove("key")

```

### Clearing Storage

Clear the entire storage:

```python
await page.shared_preferences.clear()

```

> **Caution:** `clear()` is a dangerous function that **removes all preferences of all Flet apps ever run by the same user**. It serves as a reminder that permanent application data shouldn't be stored in client storage if it cannot be easily recreated.