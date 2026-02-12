# Navigation and Routing

Navigation and routing are essential features of Single Page Applications (SPA). They allow organizing the application user interface into virtual pages (views) and "navigating" between them while the application URL reflects the current state of the app.

For mobile apps, navigation and routing serve as **deep linking** to specific application parts.

Flet's implementation is based on **Navigator 2.0 Flutter API** and replaces Flet's "Page" abstraction with "Page and Views". This offers substantial improvements:

* Programmatic control over the history stack.
* An easy way to intercept a call to the "Back" button in the AppBar.
* Robust synchronization with browser history.

## Page Route

The Page route is the portion of the application URL after the `#` symbol.

* The default application route is `/`.
* All routes start with `/` (e.g., `/store`, `/authors/1/books/2`).

### Accessing the Route

The application route can be obtained by reading the `page.route` property.

```python
import flet as ft

def main(page: ft.Page):
    page.add(ft.Text(f"Initial route: {page.route}"))

ft.run(main, view=ft.AppView.WEB_BROWSER)

```

**Testing:** Grab the application URL, open a new browser tab, paste the URL, modify the part after `#` to `/test` and hit enter. You should see "Initial route: /test".

### Handling Route Changes

Every time the route in the URL is changed (by editing the URL or navigating browser history with Back/Forward buttons), Flet calls the `page.on_route_change` event handler.

```python
import flet as ft

def main(page: ft.Page):
    page.add(ft.Text(f"Initial route: {page.route}"))

    def route_change(e: ft.RouteChangeEvent):
        page.add(ft.Text(f"New route: {e.route}"))

    page.on_route_change = route_change
    page.update()

ft.run(main, view=ft.AppView.WEB_BROWSER)

```

### Changing Route Programmatically

The route can be changed programmatically by updating the `page.route` property.

```python
import flet as ft

def main(page: ft.Page):
    page.add(ft.Text(f"Initial route: {page.route}"))

    def route_change(e: ft.RouteChangeEvent):
        page.add(ft.Text(f"New route: {e.route}"))

    def go_store(e):
        page.route = "/store"
        page.update()

    page.on_route_change = route_change
    page.add(ft.Button("Go to Store", on_click=go_store))

ft.run(main, view=ft.AppView.WEB_BROWSER)

```

---

## Page Views

Flet's `Page` is not just a single page, but a container for `View` objects layered on top of each other like a sandwich (Stack).

* A collection of views represents the **navigator history**.
* `page.views` property provides access to the views collection.
* The **last view** in the list is the one currently displayed.
* The views list must have at least one element (root view).

**Simulation of Navigation:**

1. **Navigate Forward:** Change `page.route` and add a new `View` to the end of the `page.views` list.
2. **Navigate Backward:** Pop the last view from the collection and change the route to the "previous" one in the `page.on_view_pop` event handler.

---

## Building Views on Route Change

To build reliable navigation, there must be a **single place** in the program that builds the list of views based on the current route. In other words, the navigation history stack must be a function of the route. This place is the `page.on_route_change` event handler.

### Complete Navigation Example

```python
import flet as ft

def main(page: ft.Page):
    page.title = "Routes Example"

    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("Flet app"), bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
                    ft.Button("Visit Store", on_click=lambda _: page.go("/store")),
                ],
            )
        )
        if page.route == "/store":
            page.views.append(
                ft.View(
                    "/store",
                    [
                        ft.AppBar(title=ft.Text("Store"), bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
                        ft.Button("Go Home", on_click=lambda _: page.go("/")),
                    ],
                )
            )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.run(main, view=ft.AppView.WEB_BROWSER)

```

**Key Methods:**

* **`page.go(route)`**: A helper method that updates `page.route`, calls `page.on_route_change`, and finally calls `page.update()`.
* **`page.on_view_pop`**: Fires when the user clicks the automatic "Back" button in the `AppBar`. It removes the last element from the views collection and navigates to the view "under" it.

---

## Route Templates

Flet offers `TemplateRoute`, a utility class based on the `repath` library. It allows matching ExpressJS-like routes and parsing their parameters (e.g., `/account/:account_id/orders/:order_id`).

### usage Example

```python
troute = TemplateRoute(page.route)

if troute.match("/books/:id"):
    print("Book view ID:", troute.id)
elif troute.match("/account/:account_id/orders/:order_id"):
    print("Account:", troute.account_id, "Order:", troute.order_id)
else:
    print("Unknown route")

```

---

## URL Strategy for Web

Flet web apps support two ways of configuring URL-based routing:

1. **Path (default)**: Paths are read and written without a hash (e.g., `fletapp.dev/path/to/view`).
2. **Hash**: Paths are read and written to the hash fragment (e.g., `fletapp.dev/#/path/to/view`).

### Configuration

To change the URL strategy, use the `route_url_strategy` parameter in `flet.run()`:

```python
ft.run(main, route_url_strategy="hash")

```

**Server Configuration:**
For Flet Server, the strategy can be configured via the `FLET_ROUTE_URL_STRATEGY` environment variable (values: `path` or `hash`).