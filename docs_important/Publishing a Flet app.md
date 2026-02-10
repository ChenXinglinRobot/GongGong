# Publishing a Flet App

The Flet CLI provides the `flet build` command to package a Flet app into a standalone executable or installable package for distribution.

---

## Prerequisites

### Platform Matrix

Use the following matrix to choose which OS to run `flet build` on for each target platform:

| Run on | apk / aab | ipa | macOS | Linux | Windows | Web |
| --- | --- | --- | --- | --- | --- | --- |
| **macOS** | ✅ | ✅ | ✅ |  |  | ✅ |
| **Windows** | ✅ |  |  |  | ✅ | ✅ |
| **Linux** | ✅ |  |  | ✅ |  | ✅ |

*(Note: Windows can build Android via WSL)*

### Flutter SDK

Flutter is required to build Flet apps. If not found in the system `PATH`, it will be automatically downloaded to `$HOME/flutter/{version}` during the first build.

> **Tip:** To check the recommended Flutter SDK version for your Flet installation:
> ```bash
> flet --version
> # OR
> uv run python -c "import flet.version; print(flet.version.flutter_version)"
> 
> ```
> 
> 

---

## Project Structure

The `flet build` command assumes a minimal project structure:

```text
📁 <project-name>
├── README.md
├── pyproject.toml
└── 📁 src
    ├── 📁 assets
    │   └── icon.png
    └── main.py

```

> **Tip:** Use `flet create <project-name>` to quickly set up this structure.

### Configuration Files

* **`pyproject.toml` (Recommended):** Used to specify dependencies and build settings.
* **`requirements.txt`:** Can be used instead of `pyproject.toml` for dependencies.
* *Note:* Do not use `pip freeze`. Hand-pick only direct dependencies.
* *Note:* If both files exist, `requirements.txt` is ignored.



---

## How It Works

When you run `flet build <target_platform>`, the pipeline follows these steps:

1. **Create Flutter Project:** Generates a project in `{flet_app_directory}/build/flutter` using a template. This shell app embeds your Python code and uses `serious_python` to run it.
2. **Copy Assets:** Copies custom icons and splash images from your `assets` folder.
* Generates icons via `flutter_launcher_icons`.
* Generates splash screens via `flutter_native_splash`.


3. **Package Python App:**
* Installs dependencies from PyPI.
* Compiles `.py` to `.pyc` (if configured).
* Adds project files (excluding those in `.gitignore` or specified excludes).


4. **Build:** Runs `flutter build <target_platform>` to produce the final binary.
5. **Output:** Copies the result to the output directory.

---

## Configuration (`pyproject.toml`)

Flet loads settings from `pyproject.toml` using dot-separated paths (e.g., `[tool.flet.app]`).

### Identity & Naming

| Setting | Description | Hierarchy (Precedence) |
| --- | --- | --- |
| **Entry Point** | The Python module that starts the app. | `--module-name` → `[tool.flet.app].module` → `"main"` |
| **Project Name** | Base identifier for bundle IDs (normalized). | `--project` → `[project].name` → Directory name |
| **Product Name** | User-facing display name (Window titles). | `--product` → `[tool.flet].product` → `--project` |
| **Artifact Name** | On-disk filename (e.g., `.exe`, `.app`). | `--artifact` → `[tool.flet.<PLATFORM>].artifact` → `--project` |
| **Org Name** | Reverse domain notation (e.g., `com.mycompany`). | `--org` → `[tool.flet.<PLATFORM>].org` → `"com.flet"` |
| **Bundle ID** | Unique app ID (e.g., `com.company.app`). | `--bundle-id` → `[tool.flet.<PLATFORM>].bundle_id` |

### Versioning

* **Build Number:** Integer used internally (must increment). Defaults to `pubspec.yaml` version if not set.
* **Build Version:** User-facing string (e.g., `1.0.0`).

### Dependencies

Dependencies are resolved in this order:

1. `[tool.poetry].dependencies` OR `[project].dependencies`
2. `[tool.flet.<PLATFORM>].dependencies` (Appended to above)
3. `requirements.txt` (If above are empty)

> **Note:** For Android/iOS, use **Source Packages** (`--source-packages`) if you need to install specific dependencies from source distributions (sdists) instead of binary wheels.

---

## Assets & UI

### Icons

Place image files in the `assets` directory. Flet automatically detects them based on filenames:

| Platform | Filename | Recommended Size |
| --- | --- | --- |
| **iOS** | `icon_ios.png` | ≥ 1024×1024 px (No alpha) |
| **Android** | `icon_android.png` | ≥ 192×192 px |
| **Web** | `icon_web.png` | ≥ 512×512 px |
| **Windows** | `icon_windows.ico` | 256×256 px |
| **macOS** | `icon_macos.png` | ≥ 1024×1024 px |

### Splash Screen

Supported on Android, iOS, and Web. Customize by placing images in `assets`.

**Fallback Order (Light Mode):**
`splash_<platform>.png` → `splash.png` → `icon.png`

**Configuration:**

* **Colors:** `--splash-color` and `--splash-dark-color`.
* **Disable:** `--no-android-splash`, `--no-ios-splash`, `--no-web-splash`.

### Other Screens

* **Boot Screen:** Shown while `app.zip` is extracted (Desktop/Mobile). Config: `[tool.flet.app.boot_screen]`.
* **Startup Screen:** Shown while Python runtime starts. Config: `[tool.flet.app.startup_screen]`.
* **Hidden Window:** Start desktop apps hidden to perform setup. Config: `hide_window_on_start = true`.

---

## Advanced Configuration

### Permissions (Mobile & macOS)

You can use predefined **bundles** in `pyproject.toml` or via CLI (`--permissions`) to automatically configure `Info.plist` and `AndroidManifest.xml`.

**Available Bundles:**

* `location`: Adds usage descriptions and access permissions.
* `camera`: Adds camera usage descriptions and hardware features.
* `microphone`: Adds record audio permissions.
* `photo_library`: Adds read/write access to media.

### Compilation & Cleanup

* **Compile:** Pre-compile `.py` files to `.pyc` to obscure code slightly and potentially improve startup.
* `--compile-app`, `--compile-packages`.


* **Cleanup:** Remove unnecessary files to reduce package size.
* `--cleanup-app`, `--cleanup-packages`.
* Use `--cleanup-app-files` with globs to exclude specific patterns (e.g., `**/*.c`).



### Deep Linking

Allows users to open your app via URLs (e.g., `myapp://open`).
Requires both **Scheme** and **Host**.

* CLI: `--deep-linking-scheme https --deep-linking-host mydomain.com`

---

## CI/CD: GitHub Actions Example

You can automate builds using GitHub Actions. Below is a comprehensive workflow example:

```yaml
name: Build Flet App

on:
  push:
  pull_request:
  workflow_dispatch:

env:
  UV_PYTHON: 3.12
  PYTHONUTF8: 1
  BUILD_NUMBER: 1
  BUILD_VERSION: 1.0.0
  FLET_CLI_NO_RICH_OUTPUT: 1

jobs:
  build:
    name: Build ${{ matrix.name }}
    runs-on: ${{ matrix.runner }}
    strategy:
      fail-fast: false
      matrix:
        include:
          - name: linux
            runner: ubuntu-latest
            build_cmd: "flet build linux --yes --verbose --build-number=$BUILD_NUMBER --build-version=$BUILD_VERSION"
            artifact_path: build/linux
            needs_linux_deps: true
          - name: windows
            runner: windows-latest
            build_cmd: "flet build windows --yes --verbose --build-number=$BUILD_NUMBER --build-version=$BUILD_VERSION"
            artifact_path: build/windows
            needs_linux_deps: false
          - name: macos
            runner: macos-latest
            build_cmd: "flet build macos --yes --verbose --build-number=$BUILD_NUMBER --build-version=$BUILD_VERSION"
            artifact_path: build/macos
            needs_linux_deps: false
          - name: web
            runner: ubuntu-latest
            build_cmd: "flet build web --yes --verbose"
            artifact_path: build/web
            needs_linux_deps: false

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup uv
        uses: astral-sh/setup-uv@v6

      - name: Install Linux dependencies
        if: matrix.needs_linux_deps
        shell: bash
        run: |
          sudo apt update
          sudo apt-get install -y --no-install-recommends clang ninja-build libgtk-3-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev pkg-config

      - name: Build app
        shell: bash
        run: uv run ${{ matrix.build_cmd }}

      - name: Upload Artifact
        uses: actions/upload-artifact@v5
        with:
          name: ${{ matrix.name }}-build-artifact
          path: ${{ matrix.artifact_path }}

```