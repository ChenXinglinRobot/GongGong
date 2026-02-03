# Gonggong app

## Run the app

### uv

Run as a desktop app:

```
uv run flet run
```

Run as a web app:

```
uv run flet run --web
```

For more details on running the app, refer to the [Getting Started Guide](https://docs.flet.dev/).

## Build the app

### Android

Build the APK using `uv` to ensure consistent dependencies:

```bash
# This command reads configuration from pyproject.toml
uv run flet build apk -vv
```
The build configuration (permissions, split_abi, etc.) is managed in pyproject.toml
For more details on building and signing `.apk` or `.aab`, refer to the [Android Packaging Guide](https://docs.flet.dev/publish/android/).

### iOS

```
flet build ipa -v
```

For more details on building and signing `.ipa`, refer to the [iOS Packaging Guide](https://docs.flet.dev/publish/ios/).

### macOS

```
flet build macos -v
```

For more details on building macOS package, refer to the [macOS Packaging Guide](https://docs.flet.dev/publish/macos/).

### Linux

```
flet build linux -v
```

For more details on building Linux package, refer to the [Linux Packaging Guide](https://docs.flet.dev/publish/linux/).

### Windows

```
flet build windows -v
```

For more details on building Windows package, refer to the [Windows Packaging Guide](https://docs.flet.dev/publish/windows/).


# Project: Alzheimer's Reminiscence Therapy App (Flet Implementation)

## 1. Project Overview
A local Python application using `flet` and `flet-video` to deliver interactive reminiscence therapy. The system features a modular topic selection system and a 4-stage video interaction loop (Query -> Natural Repeat -> Feedback).

## 2. Tech Stack & Constraints
- **Language**: Python 3.10+
- **GUI Framework**: Flet (Latest version)
- **Video Component**: `flet_video`
- **Strict Syntax Rules**:
  - Entry point: `ft.run(main, assets_dir="assets")`
  - Button content: `ft.FilledButton(content=ft.Text("Label"))` (No `text` param)
  - Styling: Use `ft.BorderRadius.all()`
  - Async: All event handlers must be `async`.


## 2. Tech Stack & Constraints
- **Language**: Python 3.10+
- **GUI Framework**: Flet (Latest version)
- **Video Component**: `flet_video`
- **Strict Syntax Rules**:
  - Entry point: `ft.run(main, assets_dir="assets")`  <-- 已更新
  - Navigation: Use `page.push_route(route)` (Avoid `page.go`) <-- 新增
  - Button content: `ft.FilledButton(content=ft.Text("Label"))` (No `text` param)
  - Styling: Use `ft.BorderRadius.all()`
  - Async: All event handlers must be `async`.

## 2. Tech Stack & Constraints
- **Language**: Python 3.10+
- **GUI Framework**: Flet (Latest version)
- **Video Component**: `flet_video`
- **Strict Syntax Rules**:
  - Entry point: `ft.run(main, assets_dir="assets")`
  - Navigation: Use `await page.push_route(route)` (Must be awaited)
  - Button content: `ft.FilledButton(content=ft.Text("Label"))` (No `text` param)
  - Styling: Use `ft.BorderRadius.all()`
  - Async: All event handlers must be `async`.
  - Icons: Use string names (e.g., ft.Icon(name="play_circle")) instead of ft.icons constants to avoid version mismatches.

## 2. Tech Stack & Constraints
- **Language**: Python 3.10+
- **GUI Framework**: Flet (Latest version)
- **Video Component**: `flet_video`
- **Strict Syntax Rules**:
  - Entry point: `ft.run(main, assets_dir="assets")`
  - Navigation: Use `await page.push_route(route)` (Must be awaited)
  - Button content: `ft.FilledButton(content=ft.Text("Label"))` (No `text` param)
  - Styling: Use `ft.BorderRadius.all()`
  - Async: All event handlers must be `async`.
  - Icons: Use `ft.Icons.XXX` (e.g., `ft.Icons.PLAY_CIRCLE`) and pass it as the first positional argument. Do NOT use `name=` or `ft.icons` (lowercase).

## 2. Tech Stack & Constraints
- **Language**: Python 3.10+
- **GUI Framework**: Flet (Latest version)
- **Video Component**: `flet_video`
- **Strict Syntax Rules**:
  - Entry point: `ft.run(main, assets_dir="assets")`
  - Navigation: Use `await page.push_route(route)` (Must be awaited)
  - Button content: `ft.FilledButton(content=ft.Text("Label"))` (No `text` param)
  - Styling: Use `ft.BorderRadius.all()`
  - Async: All event handlers must be `async`.
  - **Icons**: Use `ft.Icons.XXX` (Capitalized `Icons`, e.g., `ft.Icons.PLAY_CIRCLE`).
  - **Colors**: Use `ft.Colors.XXX` (Capitalized `Colors`, e.g., `ft.Colors.BLUE_400`) or Hex strings (e.g., `"#0000FF"`). Do NOT use `ft.colors` (lowercase).

## 2. Tech Stack & Constraints
- **Language**: Python 3.10+
- **GUI Framework**: Flet (Latest version)
- **Video Component**: `flet_video`
- **Strict Syntax Rules**:
  - Entry point: `ft.run(main, assets_dir="assets")`
  - Navigation: Use `await page.push_route(route)` inside `async def` handlers (NO lambdas).
  - **Naming Convention (The Golden Rule)**:
    - **Classes/Enums** (PascalCase): `ft.Icons`, `ft.Colors`, `ft.Row`, `ft.ElevatedButton`.
    - **Props/Methods** (snake_case): `size`, `on_click`, `expand`.
  - Icons: Use `ft.Icons.XXX`.
  - Colors: Use `ft.Colors.XXX`.

## 2. Tech Stack & Constraints
- **Language**: Python 3.10+
- **GUI Framework**: Flet (Latest version)
- **Video Component**: `flet_video`
- **Strict Syntax Rules**:
  - Entry point: `ft.run(main, assets_dir="assets")`
  - Navigation: Use `await page.push_route(route)` (Must be awaited)
  - Button content: `ft.FilledButton(content=ft.Text("Label"))` (No `text` param)
  - Styling: Use `ft.BorderRadius.all()`
  - Async: All event handlers must be `async`.
  - **Icons**: Use `ft.Icons.XXX` (Capitalized `Icons`, e.g., `ft.Icons.PLAY_CIRCLE`).
  - **Colors**: Use `ft.Colors.XXX` (Capitalized `Colors`, e.g., `ft.Colors.BLUE_400`) or Hex strings.
  - **Alignment**: Use explicit `ft.Alignment(x, y)` (e.g., `ft.Alignment(0, 0)` for center). Do NOT use `ft.alignment.center` constants to avoid AttributeErrors.


## 2. Tech Stack & Constraints
- **Language**: Python 3.10+
- **GUI Framework**: Flet (Latest version)
- **Video Component**: `flet_video` (Separate Package)
- **Strict Syntax Rules**:
  - Entry point: `ft.run(main, assets_dir="assets")`(Executed from `src/` context)
  - Navigation: Use `await page.push_route(route)` (Must be awaited)
  - Button content: `ft.FilledButton(content=ft.Text("Label"))` (No `text` param)
  - Styling: Use `ft.BorderRadius.all()`
  - Async: All event handlers must be `async`.
  - **Icons**: Use `ft.Icons.XXX`.
  - **Colors**: Use `ft.Colors.XXX`.
  - **Alignment**: Use `ft.Alignment(0, 0)`.

### Key Implementation Details (重要实现细节)
- **Video Force Re-render Strategy**: 
  To solve video caching/freezing issues on Android & Web, we use a **"Container Swap"** pattern. When switching videos, we do **not** update the playlist of an existing player. Instead, we create a **fresh** `ftv.Video` instance and replace the container's content. This guarantees the video engine resets completely.
## 3. Directory Structure
The application must strictly adhere to the following file structure for dynamic asset loading:
逆天了，我的电脑里面用户名有个空格，所以flutter不识别，只能用把文件夹放在d盘，用这个命令配置环境变量：set PATH=D:\flutter\bin;%PATH%，靠，还不行文件路径要小心啊，set PATH=D:\flutter\3.38.7\bin;%PATH%（中间多了一个版本号）
flutter doctor --android-licenses（安卓的协议哗啦啦的流，同意都来不及按）
set JAVA_HOME=D:\java\17.0.13+11  java在c盘的有空格文件夹中没办法，只能在d盘弄一个没有空格的
set ANDROID_HOME=D:\Android\sdk
flutter config --android-sdk "D:\Android\sdk"



```text
Gonggong/                       # Project Root
│
├── .github/workflows/          # CI/CD Automation
│   └── build_apk.yml           # GitHub Actions workflow for Android APK
│
├── pyproject.toml              # [CORE] Dependencies, Build Config & Permissions
├── uv.lock                     # Dependency Lockfile (Do not edit manually)
├── README.md                   # Project Documentation
├── .gitignore                  # Git Ignore Rules
│
└── src/                        # Source Code Root
    │
    ├── assets/                 # Media Assets Directory (Auto-scanned)
    │   │
    │   ├── topic_family/       # [Topic Folder: Family Memories]
    │   │   ├── q1_0_query.mp4     # Q1: Initial Question (State 0)
    │   │   ├── q1_1_repeat.mp4    # Q1: Gentle Repetition (State 1)
    │   │   ├── q1_2_correct.mp4   # Q1: Positive Feedback (State 2)
    │   │   └── q1_3_guide.mp4     # Q1: Guidance/Comfort (State 3)
    │   │
    │   ├── topic_music/        # [Topic Folder: Old Songs]
    │   │   └── ...
    │   │
    │   ├── icon.png            # App Icon
    │   └── splash_android.png  # Splash Screen
    │
    ├── main.py                 # Entry Point: App lifecycle & Routing logic
    ├── views.py                # UI Layer: Menu, Player, and Control Views
    ├── data_loader.py          # Data Layer: Scans /assets and builds Topic objects
    └── create_files.py         # Utility: Helper scripts for file generation
```
## 4. Naming Convention & Data Model
The `data_loader.py` module must auto-discover content based on filenames found in the `assets/` directory.

### Filename Rules
**Regex Format:** `q{sequence_id}_{type_id}_{desc}.mp4`

* **sequence_id**: Integer (1, 2, 3...), determines the order of questions within a topic.
* **type_id**: Integer (0-3), determines the video role.
    * `0`: **Query** (Initial Question / 初始提问)
    * `1`: **Repeat** (Natural Repetition / 自然重复)
    * `2`: **Correct** (Positive Feedback / 正确反馈)
    * `3`: **Guide** (Guidance or Comfort / 引导反馈)
* **desc**: String (Optional description for human readability, e.g., "ask_name").

### Data Structure (Python Representation)
The scanner should organize data into these structures:

```python
from typing import Dict, List
from dataclasses import dataclass

@dataclass
class Question:
    id: int  # Corresponds to sequence_id
    # Key is type_id (0-3), Value is the absolute file path
    videos: Dict[int, str] 

    def is_valid(self) -> bool:
        """Returns True if all 4 video types (0-3) are present."""
        return all(k in self.videos for k in [0, 1, 2, 3])

@dataclass
class Topic:
    id: str            # Folder name (e.g., "topic_family")
    name: str          # Display name (e.g., "Family Memories")
    questions: List[Question] # List of Question objects, sorted by id
```

## 5. Interaction Logic (State Machine)
The Player View operates on a specific `Question` object and manages 4 states corresponding to `type_id`.

### State 0: Query (提问)
* **Action**: Autoplay `Video[0]` (Initial Question).
* **UI Controls**:
  * Button **[听不清/再说一遍]** -> Transition to **State 1**.
  * Button **[回答正确]** -> Transition to **State 2**.
  * Button **[忘记了]** -> Transition to **State 3**.

### State 1: Repeat (自然重复)
* **Action**: Play `Video[1]` (Gentle Repetition).
* **UI Controls**:
  * Same as **State 0** (User can answer or ask to repeat again after listening).

### State 2: Correct (正确反馈)
* **Action**: Play `Video[2]` (Positive Feedback).
* **UI Controls**:
  * Button **[下一题]** -> Load next `Question` object (State 0).
  * *(If last question)* Button **[返回菜单]** -> Exit to Menu.

### State 3: Guide (引导/错误反馈)
* **Action**: Play `Video[3]` (Guidance/Comfort).
* **UI Controls**:
  * Button **[重试]** -> Reload current `Question` (State 0).
  * Button **[跳过]** -> Load next `Question` object (State 0).




## 6、奇怪的bug：
### 协议没法同意，滚太快了根本不让按y来同意


别灰心！我们遇到了一个经典的“死锁”：

Flet 帮你下了 SDK 的核心（cmdline-tools），但因为你打断了，它没来得及下载剩下的“肢体”（platform-tools）。

Flutter 检查 SDK 时，发现它“缺胳膊少腿”（没有 platform-tools），所以直接报错说“找不到 SDK”。

你想签协议补救，但 Flutter 找不到 SDK，所以也不让你签。

🔨 破局方案：绕过 Flutter，直接用 Android 原生工具
既然 Flutter 嫌弃它不完整，我们就直接用已经下载好的 Android 原生工具（sdkmanager）来手动修补。

请严格按照以下步骤操作，不需要重新下载，也不需要拼手速。

第一步：手动安装缺失的组件
在你的 CMD 黑框里，直接复制并运行下面这行命令。它会调用 D 盘里现有的工具，去下载 Flutter 缺失的那部分：

D:\Android\sdk\cmdline-tools\12.0\bin\sdkmanager.bat "platforms;android-36" "build-tools;28.0.3"

flutter doctor --android-licenses

### 代理

(GongGong) D:\update_gonggong\GongGong>

(GongGong) D:\update_gonggong\GongGong>set http_proxy=http://127.0.0.1:7897

(GongGong) D:\update_gonggong\GongGong>set https_proxy=http://127.0.0.1:7897

(GongGong) D:\update_gonggong\GongGong>curl ipinfo.io
{
  "status": 429,
  "error": {
    "title": "Rate limit exceeded",
    "message": "You've hit the daily limit for the unauthenticated API.  Create an API access token by signing up to get 50k req/month."
  }
}
(GongGong) D:\update_gonggong\GongGong>curl ifconfig.me
23.247.137.216
(GongGong) D:\update_gonggong\GongGong>curl ci.ipify.org

(GongGong) D:\update_gonggong\GongGong>rmdir /s /q build

(GongGong) D:\update_gonggong\GongGong>set PIP_INDEX_URL=

(GongGong) D:\update_gonggong\GongGong>set PUB_HOSTED_URL=

(GongGong) D:\update_gonggong\GongGong>set FLUTTER_STORAGE_BASE_URL=

(GongGong) D:\update_gonggong\GongGong>flet build apk -vv