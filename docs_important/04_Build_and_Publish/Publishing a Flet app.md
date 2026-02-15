这是一个结构化、清晰且易于AI与人类阅读的Markdown格式文档，基于你提供的“Publishing a Flet app”内容进行了整理。

---

# Publishing a Flet app

Flet CLI provides the `flet build` command to package a Flet app into a standalone executable or installable package for distribution.

## Prerequisites

### Platform Matrix

Use the following matrix to choose which OS to run `flet build` on for each target platform:

| Run on | apk / aab | ipa | macos | linux | windows | web |
| --- | --- | --- | --- | --- | --- | --- |
| **macOS** | ✅ | ✅ | ✅ |  |  | ✅ |
| **Windows** | ✅ |  |  |  | ✅ | ✅ |
| **Linux** | ✅ |  |  | ✅ |  | ✅ |

> **Note:** On Windows, Android builds (`apk`/`aab`) are supported via WSL.

### Flutter SDK

**Flutter** is required to build Flet apps for any platform.
If the minimum required version of the Flutter SDK is not already available in the system `PATH`, it will be automatically downloaded and installed (in the `$HOME/flutter/{version}` directory) during the first build process.

> **Tip:** The recommended (minimum required) Flutter SDK version depends on the Flet version installed.
> You can view it by running:
> ```bash
> flet --version
> # OR
> uv run python -c "import flet.version; print(flet.version.flutter_version)"
> # OR
> python -c "import flet.version; print(flet.version.flutter_version)"
> 
> ```
> 
> 

---

## Project Structure

The `flet build` command assumes the following minimal Flet project structure:

```text
📁 .
├── README.md
├── pyproject.toml
└── 📁 src
    ├── 📁 assets
    │   └── icon.png
    └── main.py

```

> **Tip:** To quickly set up a project with the correct structure, use:
> `flet create <project-name>`

### Using `requirements.txt`

Instead of `pyproject.toml`, you can use `requirements.txt`.

* If both files are present, `flet build` will **ignore** `requirements.txt`.
* **Do not** use `pip freeze > requirements.txt`. Hand-pick only direct dependencies (including `flet`) to avoid platform incompatibilities.

---

## How it works

When you run `flet build <target_platform>`, the pipeline is:

1. **Create Flutter Project:** Creates a project in `{flet_app_directory}/build/flutter` from a template. This embeds your Python app and uses `serious_python` to render the UI. (Cached for rapid iteration; use `--clear-cache` to force rebuild).
2. **Copy Assets:** Copies custom icons and splash images from `assets` to the Flutter project.
* Generates icons via `flutter_launcher_icons`.
* Generates splash screens via `flutter_native_splash`.


3. **Package Python App:** Uses `serious_python` package.
* Installs dependencies from PyPI (or configured sources).
* Compiles `.py` to `.pyc` (if configured).
* Adds project files (except excluded ones) to app assets.


4. **Build:** Runs `flutter build <target_platform>`.
5. **Output:** Copies artifacts to the output directory.

---

## Configuration Options

**Placeholders used below:**

* `<target_platform>`: `apk`, `aab`, `ipa`, `web`, `macos`, `windows`, `linux`.
* `<PLATFORM>`: Config namespace (e.g., `android`, `ios`, `web`, `macos`, `windows`, `linux`).
* `<flet_app_directory>`: Project root containing `pyproject.toml`.

### `pyproject.toml` Structure

Settings can be nested or dot-separated.

* **Form 1 (Preferred):** `[tool.flet.section] key = "value"`
* **Form 2:** `[tool.flet] section.key = "value"`

### Core Properties

| Property | Description | Resolution Order | Example |
| --- | --- | --- | --- |
| **App path** | Root directory of Python app. | 1. `[tool.flet.app].path`<br>

<br>2. `<python_app_path>` | `path = "src"` |
| **Entry point** | Python module starting the app. | 1. `--module-name`<br>

<br>2. `[tool.flet.app].module`<br>

<br>3. `"main"` | `module = "app.py"` |
| **Project name** | Internal base identifier (normalized). | 1. `--project`<br>

<br>2. `[project].name`<br>

<br>3. Directory name | `name = "my_app"` |
| **Product name** | User-facing display name. | 1. `--product`<br>

<br>2. `[tool.flet].product`<br>

<br>3. `--project`... | `product = "My App"` |
| **Artifact name** | On-disk name for exe/bundle. | 1. `--artifact`<br>

<br>2. `[tool.flet.<PLATFORM>].artifact`<br>

<br>3. `--project`... | `artifact = "My App"` |

### Platform Specific Metadata

| Property | Platform | Description | Resolution Order |
| --- | --- | --- | --- |
| **Organization** | Mobile/Desktop | Reverse domain notation (Prefix for Bundle ID). | 1. `--org`<br>

<br>2. `[tool.flet].org`<br>

<br>3. `"com.flet"` |
| **Bundle ID** | Mobile/Desktop | Unique App ID. | 1. `--bundle-id`<br>

<br>2. `[tool.flet].bundle_id`<br>

<br>3. Derived from Org+Project |
| **Company** | Win/Mac | Displayed in "About" dialogs. | 1. `--company`<br>

<br>2. `[tool.flet].company` |
| **Copyright** | Win/Mac | Copyright text. | 1. `--copyright`<br>

<br>2. `[tool.flet].copyright` |

### Versioning

| Property | Description | Resolution Order |
| --- | --- | --- |
| **Build Number** | Integer. Must increment for new builds. | 1. `--build-number`<br>

<br>2. `[tool.flet].build_number`<br>

<br>3. `pubspec.yaml` |
| **Build Version** | String (`x.y.z`). User-facing version. | 1. `--build-version`<br>

<br>2. `[project].version`<br>

<br>3. `[tool.poetry].version`<br>

<br>4. `pubspec.yaml` |

### Dependencies

**App Dependencies Resolution:**

1. `[tool.poetry].dependencies` OR `[project].dependencies`
2. APPEND `[tool.flet.<PLATFORM>].dependencies`
3. Fallback: `requirements.txt`
4. Fallback: `flet==<version>`

**Source Packages (Android/iOS only):**
Allows installing specific dependencies from source distributions (sdists) instead of binary wheels.

* Config: `[tool.flet].source_packages = ["pkg1", "pkg2"]`

---

## Assets

### Icons

Place image files in the `assets` directory. If platform-specific icon is missing, `icon.png` is used.

| Platform | File Name | Size | Note |
| --- | --- | --- | --- |
| **iOS** | `icon_ios.png` | ≥ 1024x1024 | No transparency allowed. |
| **Android** | `icon_android.png` | ≥ 192x192 |  |
| **Web** | `icon_web.png` | ≥ 512x512 |  |
| **Windows** | `icon_windows.ico` | 256x256 | .png automatically converted to .ico. |
| **macOS** | `icon_macos.png` | ≥ 1024x1024 |  |

### Splash Screen

Supported on **Android, iOS, Web**. Place in `assets`.

**Fallback Order:**

* **Dark:** `splash_dark_<plat>.png` → `splash_dark.png` → `splash_<plat>.png` → `splash.png` → `icon.png`
* **Light:** `splash_<plat>.png` → `splash.png` → `icon.png`

**Configuration:**

```toml
[tool.flet.splash]
color = "#ffffff"
dark_color = "#333333"
android = false  # Disable splash

```

### Other Screens (Win/Mac/Linux/Mobile)

* **Boot Screen:** Shown while app extracts.
* **Startup Screen:** Shown while Python runtime starts.

```toml
[tool.flet.app.boot_screen]
show = true
message = "Preparing..."

```

* **Hidden Window (Desktop):** Start hidden to perform setup.
* `[tool.flet.app].hide_window_on_start = true`



---

## Advanced Configuration

### Deep Linking (Mobile)

Requires both Scheme and Host.

```toml
[tool.flet.deep_linking]
scheme = "https"
host = "mydomain.com"

```

### Target Architecture (Android/macOS)

Build for specific CPU architectures to reduce size.

```toml
[tool.flet.macos]
target_arch = ["arm64", "x86_64"]

```

### Exclusion & Compilation

* **Exclude:** `[tool.flet.app].exclude = [".git", ".venv"]`
* **Compilation:** Compile `.py` to `.pyc` or clean up junk files.

```toml
[tool.flet.compile]
app = true        # Compile app files
packages = true   # Compile site-packages

```

### Permissions (Mobile/macOS)

Flet provides "bundles" to simplify permission configuration.

| Bundle | Features |
| --- | --- |
| `location` | Adds Location usage descriptions (iOS/Mac) and Access permissions (Android). |
| `camera` | Adds Camera usage descriptions (iOS/Mac) and Hardware permissions (Android). |
| `microphone` | Adds Microphone usage descriptions (iOS/Mac) and Record Audio permissions (Android). |
| `photo_library` | Adds Photo Library usage (iOS/Mac) and Read Media permissions (Android). |

**Usage:**

```toml
[tool.flet]
permissions = ["location", "microphone"]

```

---

## Build Templates

Flet uses a `cookiecutter` template to generate the Flutter project.

| Property | Description | Default |
| --- | --- | --- |
| **Source** | URL/Path to template. | `gh:flet-dev/flet-build-template` |
| **Reference** | Branch/Tag/Commit. | `<flet_version>` |
| **Directory** | Subdirectory in repo. | Root |

```toml
[tool.flet.template]
url = "gh:flet-dev/flet-build-template"
ref = "main"

```

## Flutter Specifics

* **Build Args:** Pass raw arguments to `flutter build`. *Use with caution.*
```toml
[tool.flet.flutter]
build_args = ["--obfuscate"]

```


* **Dependencies:** Override `pubspec.yaml` entries.
```toml
[tool.flet.flutter.pubspec.dependencies]
pkg_1 = "^1.2.3"

```



---

## Logging & CI/CD

### Verbose Logging

* Use `-v` or `-vv` with `flet build` for detailed output.
* **Console Output:** Python `print` and `logging` are redirected to `console.log` in packaged apps.
* **Debug:** `sys.exit(100)` shows the log in a scrollable window.

### CI/CD (GitHub Actions)

You can automate builds using GitHub Actions. Below is a summarized workflow structure:

```yaml
name: Build Flet App
# ... triggers ...
jobs:
  build:
    strategy:
       matrix:
         include:
           - name: linux
             runner: ubuntu-latest
             build_cmd: "flet build linux ..."
           - name: apk
             runner: ubuntu-latest
             build_cmd: "flet build apk ..."
           # ... other platforms ...
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v6
      - name: Install Linux dependencies
        if: matrix.needs_linux_deps
        run: |
           # ... apt-get install GStreamer, GTK, etc ...
      - name: Build app
        run: uv run ${{ matrix.build_cmd }}
      - uses: actions/upload-artifact@v5

```