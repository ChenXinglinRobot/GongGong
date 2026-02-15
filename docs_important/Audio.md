# Audio

Allows playing audio in Flet apps.

**Inherits:** `Service`

## Platform Support

| Platform | Windows | macOS | Linux | iOS | Android | Web |
| --- | --- | --- | --- | --- | --- | --- |
| **Supported** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

## Usage

To use the `Audio` control, add the `flet-audio` package to your project dependencies:

```bash
# Using uv
uv add flet-audio

# Using pip
pip install flet-audio

```

### Linux Requirements

To play audio on Linux (or WSL), you need to install the **GStreamer** library.

**Minimal installation (Ubuntu/Debian):**

```bash
sudo apt install libgtk-3-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev

```

**Full installation (Recommended for WSL or if errors occur):**

```bash
sudo apt install \
  libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgstreamer-plugins-bad1.0-dev \
  gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad \
  gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-doc gstreamer1.0-tools \
  gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 \
  gstreamer1.0-qt5 gstreamer1.0-pulseaudio

```

> **Note:** If you receive `error while loading shared libraries: libgstapp-1.0.so.0`, it means GStreamer is not installed in your WSL environment. Install the full set of GStreamer libs as shown above.

---

## Examples

### Basic Example

```python
import flet as ft
import flet_audio as fta

def main(page: ft.Page):
    url = "https://github.com/mdn/webaudio-examples/blob/main/audio-analyser/viper.mp3?raw=true"

    async def play(e):
        await audio.play()

    async def pause(e):
        await audio.pause()

    async def resume(e):
        await audio.resume()

    async def release(e):
        await audio.release()

    def set_volume(value: float):
        audio.volume += value
        audio.update()

    def set_balance(value: float):
        audio.balance += value
        audio.update()

    async def seek_2s(e):
        await audio.seek(ft.Duration(seconds=2))

    async def get_duration(e):
        duration = await audio.get_duration()
        print("Duration:", duration)

    async def on_get_current_position(e):
        position = await audio.get_current_position()
        print("Current position:", position)

    audio = fta.Audio(
        src=url,
        autoplay=False,
        volume=1,
        balance=0,
        release_mode=fta.ReleaseMode.STOP,
        on_loaded=lambda _: print("Loaded"),
        on_duration_change=lambda e: print("Duration changed:", e.duration),
        on_position_change=lambda e: print("Position changed:", e.position),
        on_state_change=lambda e: print("State changed:", e.state),
        on_seek_complete=lambda _: print("Seek complete"),
    )

    page.add(
        audio, # Important: Add audio control to the page
        ft.Button("Play", on_click=play),
        ft.Button("Pause", on_click=pause),
        ft.Button("Resume", on_click=resume),
        ft.Button("Release", on_click=release),
        ft.Button("Seek 2s", on_click=seek_2s),
        ft.Row(
            controls=[
                ft.Button("Volume down", on_click=lambda _: set_volume(-0.1)),
                ft.Button("Volume up", on_click=lambda _: set_volume(0.1)),
            ]
        ),
        ft.Row(
            controls=[
                ft.Button("Balance left", on_click=lambda _: set_balance(-0.1)),
                ft.Button("Balance right", on_click=lambda _: set_balance(0.1)),
            ]
        ),
        ft.Button("Get duration", on_click=get_duration),
        ft.Button("Get current position", on_click=on_get_current_position),
    )

ft.run(main)

```

---

## Properties

| Property | Type | Default | Attribute Metadata | Description |
| --- | --- | --- | --- | --- |
| **`autoplay`** | `bool` | `False` | `class-attribute`<br>

<br>`instance-attribute` | Starts playing audio as soon as audio control is added to a page.<br>

<br>**Note:** Works on desktop/mobile/Safari, but generally not in Chrome/Edge. |
| **`balance`** | `Number` | `0.0` | `class-attribute`<br>

<br>`instance-attribute` | Defines the stereo balance.<br>

<br>`-1`: Left channel full volume.<br>

<br>`1`: Right channel full volume.<br>

<br>`0`: Both channels same volume. |
| **`playback_rate`** | `Number` | `1.0` | `class-attribute`<br>

<br>`instance-attribute` | Defines the playback rate.<br>

<br>**Note:** iOS/macOS limits: 0.5x - 2x. Android SDK >= 23 required. |
| **`release_mode`** | `ReleaseMode` | `RELEASE` | `class-attribute`<br>

<br>`instance-attribute` | Defines the release mode (e.g., `STOP`, `RELEASE`, `LOOP`). |
| **`src`** | `str` | `bytes` | `None` | `None` |
| **`volume`** | `Number` | `1.0` | `class-attribute`<br>

<br>`instance-attribute` | Sets the volume (amplitude).<br>

<br>Range: `0.0` (mute) to `1.0` (max). |

---

## Events

| Event | Attribute Metadata | Description |
| --- | --- | --- |
| **`on_duration_change`** | `class-attribute`<br>

<br>`instance-attribute` | Fires as soon as audio duration is available. |
| **`on_loaded`** | `class-attribute`<br>

<br>`instance-attribute` | Fires when an audio is loaded/buffered. |
| **`on_position_change`** | `class-attribute`<br>

<br>`instance-attribute` | Fires when audio position is changed. Updates every 1 second if playing. |
| **`on_seek_complete`** | `class-attribute`<br>

<br>`instance-attribute` | Fires as soon as the audio seek is finished. |
| **`on_state_change`** | `class-attribute`<br>

<br>`instance-attribute` | Fires when audio player state changes (e.g., playing, paused, stopped). |

---

## Methods

### `get_current_position`

```python
get_current_position() -> Duration | None

```

Get the current position of the audio playback.

### `get_duration`

```python
get_duration() -> Duration | None

```

Get the duration of the audio playback. Available once the audio is loaded/buffered.

### `pause`

```python
pause()

```

Pauses the audio that is currently playing. Calling `resume()` later will continue from this point.

### `play`

```python
play(position: DurationValue = 0)

```

Starts playing audio from the specified `position`.

* **Parameters:**
* `position` (DurationValue): The position to start playback from. Default is `0`.



### `release`

```python
release()

```

Releases the resources associated with this media player. Resources will be fetched again if you change the source or call `resume()`.

### `resume`

```python
resume()

```

Resumes the audio that has been paused or stopped.

### `seek`

```python
seek(position: DurationValue)

```

Moves the cursor to the desired position.

* **Parameters:**
* `position` (DurationValue): The position to seek/move to.