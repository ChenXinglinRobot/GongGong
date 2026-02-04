# 公公的留声机 (GongGong)

> 为阿尔茨海默症患者定制的互动式回忆疗法应用

## 📌 项目简介

本项目是一款基于 Flet 框架开发的本地化 Python 应用，通过视频互动的方式为阿尔茨海默症患者提供回忆疗法。系统采用模块化话题选择机制，每个话题包含多个问题，每个问题通过 4 个阶段的视频进行交互式引导（提问 → 重复 → 反馈 → 引导）。

**当前状态**:
- ✅ **桌面端 (Windows)**: 运行完美，视频播放正常。
- ✅ **移动端 (Android)**: **黑屏问题彻底修复**。资源打包与路径加载逻辑已验证通过。
- ✅ **系统兼容性**: 已解决 Windows 用户名包含空格导致的路径转义错误。
2026-02-03 更新: 修复了 Windows 平台下的视频播放黑屏问题（通过绝对路径引用绕过解码器限制）。Android 端的路径适配代码已同步更新，正在进行构建测试。
2026-02-04 更新: 安卓端的路径也改成了强制路径，视频正常播放
---

## 🛠 技术栈与核心架构

### 🛠 关键架构更新：全平台统一绝对路径策略 (v0.9.0 Stable)

针对 Android 和 Windows 端的视频黑屏问题，经历了从“Web 相对路径”到“混合策略”再到“全平台绝对路径”的迭代，最终确立了以下方案：

#### ❌ 之前的错误认知 (已废弃)
- **误区 1**: 认为 Android 端的 Flet 是纯 Web 容器，必须使用 `/topic/...` 或 `/assets/...` 这样的 HTTP 风格相对路径。
  - **后果**: 播放器无法在本地文件系统中找到资源，导致黑屏。
- **误区 2**: 认为 `pyproject.toml` 不需要显式指定 `assets_dir`，只要代码里写了就行。
  - **后果**: GitHub Actions 构建出的 APK 包里只有代码，**没有视频文件**（资源丢失）。

#### ✅ 当前的正确方案 (Unified Absolute Path Strategy)
Flet 在 Android 上本质是运行在本地的 Python 环境，资源被解压到了手机的物理存储中。因此，我们采用**“邻居查找法”**：

1.  **物理路径定位**: 
    - 不依赖 Flet 的资源映射机制，而是利用 `pathlib` 获取 `views.py` 脚本的绝对路径。
    - 基于脚本位置，寻找同级目录下的 `assets` 文件夹。
    
2.  **统一 URI 协议**:
    - 全平台（Windows/Android）统一将路径转换为 **`file:///`** 协议。
    - Android 的 ExoPlayer 完美支持此协议读取本地私有目录文件。

**核心代码逻辑 (`views.py`)**:
```python
# 获取脚本所在目录的父级，拼接资源路径，并转为 file:/// URI
current_dir = pathlib.Path(__file__).parent.resolve()
full_path = current_dir.joinpath(raw_path).resolve()
return full_path.as_uri()
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
# 🔥 关键修正：必须指定 assets 的物理路径，否则视频不会被打入 APK 包！
assets_dir = "src/assets"

[tool.flet.android]
split_per_abi = false           # false = 通用包，true = 按架构分包

[tool.flet.android.permission]
"android.permission.INTERNET" = true
"android.permission.READ_EXTERNAL_STORAGE" = true
```

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

### 2026-02-04: UI 优化与视频播放器改进
- **全局窗口设置**:
  - 移除页面内边距 (`page.padding = 0`)，实现全沉浸式体验
  - 设置背景色为黑色 (`page.bgcolor = ft.Colors.BLACK`)，提供影院式边框
  - 确保不创建默认的系统应用栏
- **菜单视图文本更新**:
  - 将副标题文本格式从“包含 {count} 个环节”改为“包含 {count} 个问题”
- **播放器视图重构**:
  - 使用三层 Stack 架构实现沉浸式覆盖：
    1. **底层**: 视频层（`ft.Container` + `ftv.Video`）
    2. **中层**: 手势检测层（`ft.GestureDetector`，支持单击切换覆盖层、双击暂停/播放）
    3. **顶层**: UI 覆盖层（`ft.Container`，包含自定义 AppBar 和底部控制栏）
  - 修复菜单隐藏逻辑：为透明覆盖层添加 `on_click=toggle_overlay`，确保点击空白区域也能关闭菜单
  - 修复双击暂停功能：使用官方 `play_or_pause()` API
  - 修复 Android 视频质量和宽高比：
    - 移除无效的 `aspect_ratio` 属性
    - 设置 `fit=ft.BoxFit.CONTAIN` 确保 16:9 视频适配屏幕（带黑边，无变形）
    - 将 `filter_quality` 从 `HIGH` 改为 `MEDIUM`，提升 Android 设备清晰度
  - 修复 SafeArea 放置：
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
