# DragUpdateEvent

**Inherits:** `Event[EventControlType]`

Represents an event that is triggered when a pointer moves while remaining in contact with the screen (drag update).

## Properties

| Property | Type | Default | Attribute Metadata | Description |
| --- | --- | --- | --- | --- |
| **`global_delta`** | `Offset` | `None` | `None` | `class-attribute`<br>

<br>`instance-attribute` |
| **`global_position`** | `Offset` | - | `class-attribute`<br>

<br>`instance-attribute` | The pointer's global position when it triggered this update. |
| **`local_delta`** | `Offset` | `None` | `None` | `class-attribute`<br>

<br>`instance-attribute` |
| **`local_position`** | `Offset` | - | `class-attribute`<br>

<br>`instance-attribute` | The local position in the coordinate system of the event receiver at which the pointer contacted the screen. |
| **`primary_delta`** | `float` | `None` | `None` | `class-attribute`<br>

<br>`instance-attribute` |
| **`timestamp`** | `Duration` | `None` | `None` | `class-attribute`<br>

<br>`instance-attribute` |