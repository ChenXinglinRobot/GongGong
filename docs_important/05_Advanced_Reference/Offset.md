# Offset

A 2D floating-point offset.

## Properties

| Property | Type | Default | Attribute Metadata | Description |
| --- | --- | --- | --- | --- |
| **`distance`** | `float` | - | `property` | The magnitude of the offset. |
| **`x`** | `Number` | `0` | `class-attribute`<br>

<br>`instance-attribute` | The horizontal offset. |
| **`y`** | `Number` | `0` | `class-attribute`<br>

<br>`instance-attribute` | The vertical offset. |

---

## Methods

### `copy`

```python
copy(*, x: Number | None = None, y: Number | None = None) -> Offset

```

Returns a copy of this object with the specified properties overridden.