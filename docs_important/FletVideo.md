# Flet Video Control

Embed a full-featured video player in your Flet app with playlist support, hardware acceleration controls, and subtitle configuration. It is powered by the `media_kit` Flutter package.

## Platform Support

| Platform | Windows | macOS | Linux | iOS | Android | Web |
| --- | --- | --- | --- | --- | --- | --- |
| **Supported** | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |

## Installation

Add the `flet-video` package to your project dependencies:

```bash
# Using uv
uv add flet-video

# Using pip
pip install flet-video

```

### Linux Requirements

`libmpv` libraries must be installed when using the `flet-video` package. These are system dependencies and must be present on the machine running the app.

On **Ubuntu/Debian**, run:

```bash
sudo apt install libmpv-dev mpv

```

If you encounter `libmpv.so.1` load errors, run:

```bash
sudo apt update
sudo apt install libmpv-dev libmpv2
sudo ln -s /usr/lib/x86_64-linux-gnu/libmpv.so /usr/lib/libmpv.so.1

```

---

## Examples

### Basic Example

```python
import random
import flet as ft
import flet_video as ftv

sample_media = [
    ftv.VideoMedia(
        "https://user-images.githubusercontent.com/28951144/229373720-14d69157-1a56-4a78-a2f4-d7a134d7c3e9.mp4"
    ),
    ftv.VideoMedia(
        "https://user-images.githubusercontent.com/28951144/229373718-86ce5e1d-d195-45d5-baa6-ef94041d0b90.mp4"
    ),
    ftv.VideoMedia(
        "https://user-images.githubusercontent.com/28951144/229373716-76da0a4e-225a-44e4-9ee7-3e9006dbc3e3.mp4"
    ),
    ftv.VideoMedia(
        "https://user-images.githubusercontent.com/28951144/229373695-22f88f13-d18f-4288-9bf1-c3e078d83722.mp4"
    ),
    ftv.VideoMedia(
        "https://user-images.githubusercontent.com/28951144/229373709-603a7a89-2105-4e1b-a5a5-a6c3567c9a59.mp4",
        extras={
            "artist": "Thousand Foot Krutch",
            "album": "The End Is Where We Begin",
        },
        http_headers={
            "Foo": "Bar",
            "Accept": "*/*",
        },
    ),
]


def main(page: ft.Page):
    page.spacing = 20
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    async def handle_pause(e: ft.Event[ft.Button]):
        await video.pause()

    async def handle_play_or_pause(e: ft.Event[ft.Button]):
        await video.play_or_pause()

    async def handle_play(e: ft.Event[ft.Button]):
        await video.play()

    async def handle_stop(e: ft.Event[ft.Button]):
        await video.stop()

    async def handle_next(e: ft.Event[ft.Button]):
        await video.next()

    async def handle_previous(e: ft.Event[ft.Button]):
        await video.previous()

    def handle_volume_change(e: ft.Event[ft.Slider]):
        video.volume = e.control.value

    def handle_playback_rate_change(e: ft.Event[ft.Slider]):
        video.playback_rate = e.control.value

    async def handle_seek(e: ft.Event[ft.Button]):
        await video.seek(10000)

    async def handle_add_media(e: ft.Event[ft.Button]):
        await video.playlist_add(random.choice(sample_media))

    async def handle_remove_media(e: ft.Event[ft.Button]):
        r = random.randint(0, len(video.playlist) - 1)
        await video.playlist_remove(r)

    async def handle_jump(e: ft.Event[ft.Button]):
        await video.jump_to(0)

    async def handle_fullscreen(e: ft.Event[ft.Button]):
        video.fullscreen = True

    page.add(
        ft.SafeArea(
            expand=True,
            content=ft.Column(
                expand=True,
                controls=[
                    video := ftv.Video(
                        expand=True,
                        playlist=sample_media[0:2],
                        playlist_mode=ftv.PlaylistMode.LOOP,
                        fill_color=ft.Colors.BLUE_400,
                        aspect_ratio=16 / 9,
                        volume=100,
                        autoplay=False,
                        filter_quality=ft.FilterQuality.HIGH,
                        muted=False,
                        on_load=lambda e: print("Video loaded successfully!"),
                        on_enter_fullscreen=lambda e: print("Entered fullscreen!"),
                        on_exit_fullscreen=lambda e: print("Exited fullscreen!"),
                    ),
                    ft.Row(
                        wrap=True,
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Button("Play", on_click=handle_play),
                            ft.Button("Pause", on_click=handle_pause),
                            ft.Button("Play Or Pause", on_click=handle_play_or_pause),
                            ft.Button("Stop", on_click=handle_stop),
                            ft.Button("Next", on_click=handle_next),
                            ft.Button("Previous", on_click=handle_previous),
                            ft.Button("Seek s=10", on_click=handle_seek),
                            ft.Button("Jump to first Media", on_click=handle_jump),
                            ft.Button("Add Random Media", on_click=handle_add_media),
                            ft.Button(
                                "Remove Random Media", on_click=handle_remove_media
                            ),
                            ft.Button("Enter Fullscreen", on_click=handle_fullscreen),
                        ],
                    ),
                    ft.Slider(
                        min=0,
                        value=100,
                        max=100,
                        label="Volume = {value}%",
                        divisions=10,
                        width=400,
                        on_change=handle_volume_change,
                    ),
                    ft.Slider(
                        min=1,
                        value=1,
                        max=3,
                        label="Playback rate = {value}X",
                        divisions=6,
                        width=400,
                        on_change=handle_playback_rate_change,
                    ),
                ],
            ),
        )
    )

ft.run(main)

```

---

## API Reference

**Inherits:** `LayoutControl`

A control that displays a video from a playlist.

### Properties

| Property | Type | Default | Description |
| --- | --- | --- | --- |
| **`alignment`** | `Alignment` | `CENTER` | Defines the Alignment of the viewport. |
| **`autoplay`** | `bool` | `False` | Whether the video should start playing automatically. |
| **`configuration`** | `VideoConfiguration` | `VideoConfiguration()` | Additional configuration for the video player. |
| **`fill_color`** | `ColorValue` | `BLACK` | Defines the color used to fill the video background. |
| **`filter_quality`** | `FilterQuality` | `LOW` | Filter quality of the texture used to render the video output.<br>

<br>**Note:** Android was reported to show blurry images when using `HIGH`. Prefer `MEDIUM` on this platform. |
| **`fit`** | `BoxFit` | `CONTAIN` | The box fit to use for the video. |
| **`fullscreen`** | `bool` | `False` | Whether the video player is presented in fullscreen mode. Set to `True` to enter fullscreen or `False` to exit programmatically. |
| **`muted`** | `bool` | `False` | Defines whether the video player should be started in muted state. |
| **`pause_upon_entering_background_mode`** | `bool` | `True` | Whether to pause the video when application enters background mode. |
| **`pitch`** | `Number` | `1.0` | Defines the relative pitch of the video player. |
| **`playback_rate`** | `Number` | `1.0` | Defines the playback rate of the video player. |
| **`playlist`** | `list[VideoMedia]` | `[]` | A list of `VideoMedia` objects representing the video files to be played. |
| **`playlist_mode`** | `PlaylistMode` | `None` | `None` |
| **`resume_upon_entering_foreground_mode`** | `bool` | `False` | Whether to resume the video when application enters foreground mode. Only has effect if `pause_upon_entering_background_mode` is `True`. |
| **`show_controls`** | `bool` | `True` | Whether to show the video player controls. |
| **`shuffle_playlist`** | `bool` | `False` | Defines whether the playlist should be shuffled. |
| **`subtitle_configuration`** | `VideoSubtitleConfiguration` | `VideoSubtitleConfiguration()` | Defines the subtitle configuration for the video player. |
| **`subtitle_track`** | `VideoSubtitleTrack` | `None` | `None` |
| **`title`** | `str` | `'flet-video'` | Defines the name of the underlying window & process for native backend. Visible inside the windows volume mixer. |
| **`volume`** | `Number` | `100.0` | Defines the volume of the video player. <br>

<br>**Note:** Ranges between `0.0` (muted) to `100.0` (max). Raises `ValueError` if outside range. |
| **`wakelock`** | `bool` | `True` | Whether to acquire wake lock while playing. When `True`, device's display will not sleep while playing. |

### Events

| Event | Type | Description |
| --- | --- | --- |
| **`on_complete`** | `ControlEventHandler[Video]` | Fires when a video player completes. |
| **`on_enter_fullscreen`** | `ControlEventHandler[Video]` | Fires when the video player enters fullscreen. |
| **`on_error`** | `ControlEventHandler[Video]` | Fires when an error occurs. `data` property contains error info. |
| **`on_exit_fullscreen`** | `ControlEventHandler[Video]` | Fires when the video player exits fullscreen. |
| **`on_load`** | `ControlEventHandler[Video]` | Fires when the video player is initialized and ready for playback. |
| **`on_track_change`** | `ControlEventHandler[Video]` | Fires when a video track changes. `data` property contains the index of the new track. |

### Methods

#### `get_current_position()`

* **Returns:** `Duration`
* **Description:** The current position of the currently playing media.

#### `get_duration()`

* **Returns:** `Duration`
* **Description:** The duration of the currently playing media.

#### `is_completed()`

* **Returns:** `bool`
* **Description:** `True` if video player has reached the end of the currently playing media, `False` otherwise.

#### `is_playing()`

* **Returns:** `bool`
* **Description:** `True` if the video player is currently playing, `False` otherwise.

#### `jump_to(media_index: int)`

* **Description:** Jumps to the `VideoMedia` at the specified `media_index` in the `playlist`.

#### `next()`

* **Description:** Jumps to the next `VideoMedia` in the `playlist`.

#### `pause()`

* **Description:** Pauses the video player.

#### `play()`

* **Description:** Starts playing the video.

#### `play_or_pause()`

* **Description:** Cycles between play and pause states (plays if paused, pauses if playing).

#### `playlist_add(media: VideoMedia)`

* **Description:** Appends/Adds the provided `media` to the `playlist`.

#### `playlist_remove(media_index: int)`

* **Description:** Removes the provided `media` from the `playlist` at the specified index.

#### `previous()`

* **Description:** Jumps to the previous `VideoMedia` in the `playlist`.

#### `seek(position: DurationValue)`

* **Description:** Seeks the currently playing `VideoMedia` to the specified `position`.

#### `stop()`

* **Description:** Stops the video player.