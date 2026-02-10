# 公公的留声机 (GongGong)

> 为阿尔茨海默症患者定制的互动式回忆疗法应用

## 📌 项目简介

本项目是一款基于 Flet 0.80.5+ 框架开发的跨平台 Python 应用，通过视频互动的方式为阿尔茨海默症患者提供回忆疗法。系统采用模块化话题选择机制，每个话题包含多个问题，每个问题通过 4 个阶段的视频进行交互式引导（提问 → 重复 → 反馈 → 引导）。

**核心特性**:
- ✅ **跨平台支持**: Windows、Android、Web
- ✅ **解耦架构**: 视频文件与安装包分离，可从外部存储加载
- ✅ **智能设置向导**: 首次启动引导用户选择视频文件夹
- ✅ **权限管理**: 自动处理 Android 存储权限请求
- ✅ **沉浸式界面**: 全屏视频播放，手势控制

**当前状态**:
- ✅ **桌面端 (Windows)**: 运行完美，支持从任意文件夹加载视频
- ✅ **移动端 (Android)**: 支持从手机存储加载视频，权限管理完善
- ✅ **Flet 0.80.5 兼容**: 已修复所有 "Unknown control" 错误
---

## 🛠 技术栈与核心架构

### 🛠 解耦架构：外部文件加载系统 (v1.0.0)

应用现在采用完全解耦的架构，视频文件不再需要打包进 APK 安装包。用户可以在首次启动时选择手机或电脑上的任意文件夹作为视频源。

#### ✅ 核心优势
- **安装包小巧**: APK 仅包含应用代码，体积大幅减小
- **灵活更新**: 更新视频内容无需重新安装应用
- **多设备共享**: 同一视频文件夹可在多台设备间共享
- **存储优化**: 视频文件可存储在外部 SD 卡或云存储中

#### 🔧 设置向导流程
1. **首次启动**: 应用检测到未配置视频路径，自动跳转到设置向导
2. **权限请求** (Android): 自动请求存储权限
3. **文件夹选择**: 使用系统文件选择器选择包含视频话题的文件夹
4. **自动验证**: 系统验证文件夹结构并加载可用话题
5. **持久化存储**: 选择的路径保存到应用配置中

#### 📱 Flet 0.80.5 API 更新
应用已完全适配 Flet 0.80.5 的新 API：
- **FilePicker**: 使用内联实例化模式，不再需要 `page.overlay.append()`
  ```python
  selected_path = await ft.FilePicker().get_directory_path(dialog_title="选择视频文件夹")
  ```
- **PermissionHandler**: 直接实例化使用，无需页面挂载
  ```python
  ph = fph.PermissionHandler()
  status = await ph.request(fph.Permission.MANAGE_EXTERNAL_STORAGE)
  ```

### 🛠 视频路径处理策略

针对 Android 和 Windows 端的视频播放，采用**统一绝对路径策略**：

#### ✅ 当前方案 (Unified Absolute Path Strategy)
Flet 在 Android 上本质是运行在本地的 Python 环境，因此我们采用**物理路径定位**：

1.  **外部文件加载**: 用户选择的文件夹路径直接作为视频源
2.  **统一 URI 协议**: 全平台统一将路径转换为 **`file:///`** 协议
3.  **Android 兼容**: ExoPlayer 完美支持 `file:///` 协议读取本地文件

**核心代码逻辑 (`views.py`)**:
```python
def _get_video_src(raw_path: str) -> str:
    """全平台通用的绝对物理路径策略"""
    full_path = pathlib.Path(raw_path).resolve()
    return full_path.as_uri()  # 返回 file:/// URI 格式
```

### 核心依赖
- **Python**: 3.10+
- **GUI 框架**: Flet 0.80.5+（基于 2026 年最新版本）
- **视频组件**: flet-video 0.80.5+
- **构建工具**: uv (依赖管理) + GitHub Actions (CI/CD)

### 关键语法规范（基于 Flet 0.80+）

> ⚠️ Flet 更新极快，以下规范基于 2026 年最新版本，如有疑问请查阅官方文档

| 类别 | 规范 | 示例 |
|------|------|------|
| **入口点** | `ft.run(main, assets_dir="assets")` | 从 `src/` 上下文执行 |
| **导航** | 必须使用 `await page.push_route(route)` | 异步函数内使用，必须 await |
| **按钮文本** | `ft.FilledButton(content=ft.Text("..."))` | ❌ 无 `text` 参数 |
| **图标** | `ft.Icons.XXX`（大写） | `ft.Icons.PLAY_CIRCLE` |
| **颜色** | `ft.Colors.XXX`（大写）或十六进制 | `ft.Colors.BLUE_400` 或 `"#0000FF"` |
| **对齐** | `ft.Alignment(x, y)` | `ft.Alignment(0, 0)` 表示居中 |
| **圆角** | `ft.BorderRadius.all(value)` | `ft.BorderRadius.all(10)` |
| **事件处理** | 所有 handler 必须是 `async def` | ❌ 不支持 lambda |

### 视频强制重渲染策略

为解决 Android/Web 端视频缓存/冻结问题，采用**"容器替换"**模式：
- ❌ 不更新现有播放器的 playlist
- ✅ 每次切换视频时创建全新的 `ftv.Video` 实例
- ✅ 替换 `Container.content` 强制视频引擎完全重置

```python
# 示例代码片段
new_player = ftv.Video(
    expand=True,
    autoplay=True,
    playlist=[ftv.VideoMedia(src)],
    key=f"video_{unique_id}"  # 确保唯一性
)
video_container.content = new_player
```

---

## 📁 项目结构

```
GongGong/
│
├── .github/workflows/          # CI/CD 自动化
│   └── build_apk.yml           # GitHub Actions 打包配置
│
├── src/                        # 源代码根目录
│   ├── main.py                 # 应用入口：生命周期 & 路由逻辑
│   ├── views.py                # UI 层：菜单视图、播放器视图
│   ├── data_loader.py          # 数据层：扫描 assets 并构建 Topic 对象
│   ├── create_files.py         # 工具脚本
│   │
│   └── assets/                 # 媒体资源目录（自动扫描）
│       ├── icon.png            # 应用图标
│       ├── splash_android.png  # 启动屏幕
│       │
│       ├── topic_naming/       # [话题文件夹示例：起名字]
│       │   ├── q1_0_ask_name.mp4     # Q1: 初始提问（State 0）
│       │   ├── q1_1_repeat_name.mp4  # Q1: 温和重复（State 1）
│       │   ├── q1_2_praise_name.mp4  # Q1: 正向反馈（State 2）
│       │   └── q1_3_guide_name.mp4   # Q1: 引导/安慰（State 3）
│       │
│       └── topic_huize/        # [话题文件夹示例：惠泽小吃]
│           └── ... (同上结构)
│
├── pyproject.toml              # 核心配置：依赖、构建参数、权限
├── uv.lock                     # 依赖锁定文件（自动生成）
├── .gitignore                  # Git 忽略规则
└── README.md                   # 本文档
```

---

## 🎯 命名规范与数据模型

### 视频文件命名规则

**格式**: `q{sequence_id}_{type_id}_{description}.mp4`

**参数说明**:
- `sequence_id`: 整数（1, 2, 3...），决定问题在话题中的顺序
- `type_id`: 整数（0-3），决定视频角色：
  - `0` → **Query** (初始提问)
  - `1` → **Repeat** (自然重复)
  - `2` → **Correct** (正确反馈)
  - `3` → **Guide** (引导/安慰)
- `description`: 字符串（可选，便于人类识别，如 "ask_name"）

**示例**:
```
q1_0_ask_name.mp4      # 第1题的初始提问
q1_1_repeat_name.mp4   # 第1题的重复
q2_0_ask_snack.mp4     # 第2题的初始提问
```

### 数据结构

```python
@dataclass
class Question:
    id: int                    # 对应 sequence_id
    videos: Dict[int, str]     # {type_id: 文件路径}
    
    def is_valid(self) -> bool:
        """验证是否包含完整的 4 个阶段视频"""
        return all(k in self.videos for k in [0, 1, 2, 3])

@dataclass
class Topic:
    id: str                    # 文件夹名（如 "topic_naming"）
    name: str                  # 显示名称（如 "起名字"）
    questions: List[Question]  # 按 id 排序的问题列表
```

---

## 🎮 交互逻辑（状态机）

播放器视图针对每个 `Question` 对象管理 4 个状态（对应 `type_id`）：

### State 0: Query（提问）
- **动作**: 自动播放 `Video[0]`（初始提问）
- **用户操作**:
  - 🔵 **听不清/再说一遍** → 转到 State 1
  - 🟢 **回答正确** → 转到 State 2
  - 🟠 **忘记了** → 转到 State 3

### State 1: Repeat（重复）
- **动作**: 播放 `Video[1]`（温和重复）
- **用户操作**: 同 State 0（可继续回答或再次请求重复）

### State 2: Correct（正确反馈）
- **动作**: 播放 `Video[2]`（正向鼓励）
- **用户操作**:
  - 🟢 **下一题** → 加载下一个 Question（返回 State 0）
  - 🏠 **返回菜单**（如果是最后一题）

### State 3: Guide（引导）
- **动作**: 播放 `Video[3]`（引导/安慰）
- **用户操作**:
  - 🔄 **重试** → 重新加载当前 Question（返回 State 0）
  - ⏭️ **跳过** → 加载下一个 Question（返回 State 0）

---

## 🚀 快速开始

### 本地运行

#### 1. 安装依赖（推荐使用 uv）

```bash
# 安装 uv（如果尚未安装）
pip install uv

# 同步依赖
uv sync
```

#### 2. 桌面模式运行

```bash
uv run flet run
```

#### 3. Web 模式运行

```bash
uv run flet run --web
```

---

## 📦 Android APK 打包

### 方式一：GitHub Actions 自动打包（✅ 推荐）

**流程说明**:
1. 推送代码到 `main` 或 `master` 分支
2. GitHub Actions 自动触发构建流程（见 `.github/workflows/build_apk.yml`）
3. 构建完成后在 **Actions** 页面下载 APK

**手动触发**:
- 进入 GitHub 仓库 → Actions → "Build Android APK" → Run workflow

**配置说明**:
- 运行环境: `ubuntu-latest`（Linux）
- Java: Temurin 17
- Flutter: Stable 通道
- 依赖管理: uv
- 构建命令: `uv run flet build apk --verbose --project "Gonggong"`

**关键优势**:
- ✅ 无需本地配置 Flutter/Android SDK
- ✅ 环境一致性有保障
- ✅ 自动化构建，可复现

### 方式二：本地打包（仅限参考）

> ⚠️ 本地 Windows 环境打包存在诸多环境依赖问题，建议优先使用 GitHub Actions

**详细的本地打包尝试记录** 请参考：[`LOCAL_BUILD_WINDOWS.md`](./LOCAL_BUILD_WINDOWS.md)

**简要步骤**:
```bash
# 确保已安装 Flutter、Android SDK、Java 17
# 清理旧构建
uv run flet build apk -vv
```

**常见问题**:
- 用户名包含空格导致 Flutter 无法识别
- 协议签署流程过快
- 环境变量配置复杂

---

## ⚙️ 配置文件说明

### pyproject.toml

核心配置文件，包含项目元信息、依赖和构建参数。

```toml
[tool.flet]
org = "com.gonggong"            # 组织标识符
product = "公公的留声机"         # 应用名称
company = "GongGong Family"     # 公司/团队名

[tool.flet.app]
path = "src"                    # 源码路径

[tool.flet.android]
split_per_abi = false           # false = 通用包，true = 按架构分包

[tool.flet.android.permission]
"android.permission.INTERNET" = true
"android.permission.READ_EXTERNAL_STORAGE" = true
"android.permission.WRITE_EXTERNAL_STORAGE" = true
"android.permission.MANAGE_EXTERNAL_STORAGE" = true  # Android 11+ 核心权限
```

**重要变化**:
- 移除了 `assets_dir` 配置，因为视频文件现在从外部存储加载
- 增加了 Android 存储权限配置，支持从外部存储读取视频文件

---

## ⚠️ 已知问题

### 视频播放黑屏

**问题描述**:
- 桌面端使用 `ft.AppView.WEB_BROWSER` 模式时视频正常
- 桌面客户端模式和 Android 应用中视频显示黑屏
- 其他功能完全正常

**当前状态**:
- 已创建 `fix/video-black-screen` 分支专门解决此问题
- 初步分析与视频编解码器/硬件加速有关

**临时解决方案**:
```python
# 在开发调试时可使用 Web 模式
ft.run(main, assets_dir="assets", view=ft.AppView.WEB_BROWSER)
```

## 📝 问题修复记录

### [已解决] Flet 0.80.5 "Unknown control" 错误 (Windows & Android)
- **症状**: 
  - Windows PC: `ft.FilePicker` 报 "Unknown control: filepicker"
  - Android APK: `flet_permission_handler` 报 "Unknown control: permission_handler"
- **根本原因**: Flet 0.80.5 API 变化，`FilePicker` 和 `PermissionHandler` 现在都是 `Service` 类型，不再需要添加到 `page.overlay`
- **修复方案**: 
  1. 重写 `main.py`，移除所有 `page.overlay.append()` 调用
  2. 重写 `views.py`，改用内联实例化 API：
     ```python
     # FilePicker - 直接实例化使用
     selected_path = await ft.FilePicker().get_directory_path()
     
     # PermissionHandler - 直接实例化使用
     ph = fph.PermissionHandler()
     status = await ph.request(permission)
     ```

### [已解决] 视频播放黑屏 (Android & Windows)
- **症状**: 界面UI加载正常，但视频区域黑屏，无报错或报 `No such file`。
- **根本原因**: 
  1. **资源丢失**: `pyproject.toml` 缺少 `assets_dir` 配置，导致视频未打包进 APK。
  2. **路径错误**: 代码使用了 Web 相对路径，而 Android ExoPlayer 需要本地绝对路径 (`file:///`)。
- **修复方案**: 
  1. 修正构建配置，确保资源打入包内。
  2. 重构 `views.py`，使用 `pathlib` 动态计算绝对物理路径。

### [已解决] Windows 用户名空格问题
- **症状**: 路径 `C:\Users\Chen Xinglin\...` 被截断或转义错误。
- **修复方案**: 同样通过 `pathlib.resolve()` 获取绝对路径并转换为 URI 解决。

## 📝 更新日志

### 2026-02-10: 解耦架构与 Flet 0.80.5 修复
- **解耦架构**:
  - 视频文件不再打包进 APK，改为从外部存储加载
  - 安装包体积大幅减小，更新视频内容无需重新安装应用
  - 支持从手机/电脑任意文件夹加载视频文件
- **智能设置向导**:
  - 首次启动自动引导用户选择视频文件夹
  - Android 自动请求存储权限
  - 自动验证文件夹结构并加载可用话题
- **Flet 0.80.5 API 适配**:
  - 修复 "Unknown control: filepicker" 错误（Windows）
  - 修复 "Unknown control: permission_handler" 错误（Android）
  - 改用内联实例化 API：`await ft.FilePicker().get_directory_path()`
  - 移除所有 `page.overlay.append()` 调用
- **权限管理优化**:
  - 自动处理 Android 存储权限请求
  - 支持 Android 11+ 的 `MANAGE_EXTERNAL_STORAGE` 权限

### 2026-02-04: UI 优化与视频播放器改进
- **全局窗口设置**:
  - 移除页面内边距 (`page.padding = 0`)，实现全沉浸式体验
  - 设置背景色为黑色 (`page.bgcolor = ft.Colors.BLACK`)，提供影院式边框
  - 确保不创建默认的系统应用栏
- **菜单视图文本更新**:
  - 将副标题文本格式从"包含 {count} 个环节"改为"包含 {count} 个问题"
- **播放器视图重构**:
  - 使用三层 Stack 架构实现沉浸式覆盖:
    1. **底层**: 视频层（`ft.Container` + `ftv.Video`）
    2. **中层**: 手势检测层（`ft.GestureDetector`，支持单击切换覆盖层、双击暂停/播放）
    3. **顶层**: UI 覆盖层（`ft.Container`，包含自定义 AppBar 和底部控制栏）
  - 修复菜单隐藏逻辑：为透明覆盖层添加 `on_click=toggle_overlay`，确保点击空白区域也能关闭菜单
  - 修复双击暂停功能：使用官方 `play_or_pause()` API
  - 修复 Android 视频质量和宽高比:
    - 移除无效的 `aspect_ratio` 属性
    - 设置 `fit=ft.BoxFit.CONTAIN` 确保 16:9 视频适配屏幕（带黑边，无变形）
    - 将 `filter_quality` 从 `HIGH` 改为 `MEDIUM`，提升 Android 设备清晰度
  - 修复 SafeArea 放置:
    - 从根 View 控件中移除 `ft.SafeArea`
    - 仅在 UI 覆盖层内部添加 `ft.SafeArea`
    - 视频堆叠层现在可以触及物理屏幕边缘
  - 清理调试文本和多余容器
- **代码优化**:
  - 修复变量引用顺序错误（`toggle_overlay` 在赋值前被引用）
  - 所有函数添加中文注释

---

## 📚 参考资源

- [Flet 官方文档](https://docs.flet.dev/)
- [Android 打包指南](https://docs.flet.dev/publish/android/)
- [flet-video 组件文档](https://flet.dev/docs/controls/video)

---

## 🤝 贡献指南

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m '添加某某功能'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 提交 Pull Request

**注意事项**:
- 所有函数必须添加中文注释
- 遵循 Flet 0.80+ 的最新语法规范
- 测试代码在桌面和 Web 模式下的兼容性

---

## 📄 许可证

Copyright (C) 2026 GongGong Family

---

## 👤 作者

GongGong Developer  
邮箱: 1641782731@qq.com
