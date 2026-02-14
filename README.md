# 公公的留声机 (GongGong)

> 为阿尔茨海默症患者定制的互动式回忆疗法应用

## 📌 项目简介

本项目是一款基于 Flet 0.80.5+ 框架开发的跨平台 Python 应用，通过视频互动的方式为阿尔茨海默症患者提供回忆疗法。系统采用**模块化架构**和话题选择机制，每个话题包含多个问题，每个问题通过 4 个阶段的视频进行交互式引导（提问 → 重复 → 反馈 → 引导）。

**核心特性**:
- ✅ **模块化架构**: 视图层分解为独立模块，提高代码可维护性
- ✅ **跨平台支持**: Windows、Android、Web
- ✅ **解耦架构**: 视频文件与安装包分离，可从外部存储加载
- ✅ **智能设置向导**: 首次启动引导用户选择视频文件夹
- ✅ **权限管理**: 自动处理 Android 存储权限请求
- ✅ **沉浸式界面**: 全屏视频播放，手势控制
- ✅ **动画化欢迎场景**: 全屏模糊背景 + 前景清晰图片 + 触觉反馈按钮
- ✅ **弧形卡片选择器**: 话题卡片沿弧线排列，支持垂直拖拽滚动
- ✅ **同步过渡动画**: 欢迎场景到话题选择的无缝过渡，左右面板同步入场
- ✅ **两步确认交互**: 选择 → 聚焦 → 进入的三态交互流程
- ✅ **实时图片预览**: 右侧实时显示选中话题的封面图片

**当前状态**:
- ✅ **桌面端 (Windows)**: 运行完美，支持从任意文件夹加载视频
- 🔄 **移动端 (Android)**: 待测试（理论上支持从手机存储加载视频）
- ✅ **Flet 0.80.5 兼容**: 已修复所有 "Unknown control" 错误
- ✅ **欢迎场景**: 已实现完整的动画过渡和交互体验
- ✅ **话题选择器**: 已升级为弧形卡片布局，支持手势操作

---

## 🏗️ 项目结构（模块化架构）

本项目采用模块化架构，将原本单一的 `views.py` 分解为独立的视图模块，提高了代码的可维护性和可扩展性。

```text
GongGong/
│
├── .github/workflows/          # CI/CD 自动化
│   └── build_apk.yml           # GitHub Actions 打包配置
│
├── src/                        # 源代码根目录
│   ├── main.py                 # 应用入口：生命周期 & 路由逻辑
│   ├── config.py               # [NEW] 配置常量模块（颜色、尺寸等）
│   ├── utils.py                # [NEW] 工具函数模块（路径处理等）
│   ├── data_loader.py          # 数据层：扫描 assets 并构建 Topic 对象
│   ├── create_files.py         # 工具脚本
│   │
│   └── views/                  # [NEW] 视图层包（模块化分解）
│       ├── __init__.py         # 导出所有视图函数
│       ├── menu.py             # 菜单视图：话题选择界面（备用）
│       ├── setup.py            # 设置向导视图：首次启动配置
│       ├── player.py           # 播放器视图：核心视频交互逻辑
│       └── welcome.py          # [NEW] 欢迎视图：动画化欢迎场景与弧形话题选择器
│
├── pyproject.toml              # 核心配置：依赖、构建参数、权限
├── uv.lock                     # 依赖锁定文件（自动生成）
├── .gitignore                  # Git 忽略规则
└── README.md                   # 本文档
```

**架构优势**:
- **关注点分离**: 每个视图模块专注于单一功能
- **易于维护**: 修改一个视图不会影响其他模块
- **代码复用**: 视图函数可以独立测试和重用
- **团队协作**: 不同开发者可以并行开发不同视图

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

#### 2. 运行应用（模块化架构的正确方式）

```bash
# 从项目根目录运行（推荐）
uv run flet run src/main.py

# 或者使用完整路径
flet run src/main.py
```

#### 3. Web 模式运行

```bash
uv run flet run src/main.py --web
```

### ⚠️ 重要提示：模块化架构的运行方式

由于项目采用了模块化架构，**必须**从项目根目录运行 `flet run src/main.py`。这是因为：

1. **相对导入**: 模块之间使用相对导入（如 `from data_loader import Topic`）
2. **Python 路径**: 需要确保 `src` 目录在 Python 路径中
3. **Flet 上下文**: Flet 需要正确的项目上下文来加载资源

**错误运行方式**:
```bash
# ❌ 错误：会导致 ModuleNotFoundError
cd src
flet run main.py

# ❌ 错误：缺少项目上下文
python src/main.py
```

---

## 🛠️ 技术架构

### 视图层分解（模块化设计）

原本单一的 `views.py` 文件已被分解为四个独立的模块：

1. **`welcome.py`** - 欢迎视图（新增）
   - 动画化欢迎场景：模糊背景 + 前景清晰图片
   - 弧形卡片话题选择器，支持垂直拖拽滚动
   - 两步确认交互流程（选择 → 聚焦 → 进入）
   - 右侧实时图片预览，与左侧卡片同步

2. **`menu.py`** - 菜单视图（备用）
   - 显示所有可用话题
   - 提供话题选择界面（作为简单备用模式）
   - 处理话题点击事件

3. **`setup.py`** - 设置向导视图
   - 首次启动引导用户选择视频文件夹
   - 处理 Android 存储权限请求
   - 验证文件夹结构并保存配置

4. **`player.py`** - 播放器视图
   - 核心视频播放和交互逻辑
   - 实现 4 阶段状态机（提问 → 重复 → 反馈 → 引导）
   - 处理手势控制和 UI 覆盖层

**分解优势**:
- **可维护性**: 每个文件约 200-400 行代码，易于理解和修改
- **可测试性**: 可以独立测试每个视图模块，如 `test_welcome.py`
- **可扩展性**: 添加新视图只需创建新模块，无需修改现有代码
- **团队协作**: 不同开发者可以并行开发不同视图
- **渐进增强**: 新增 `welcome.py` 不影响原有功能，`menu.py` 作为备用

### 状态机（4 阶段视频交互逻辑）

播放器视图针对每个 `Question` 对象管理 4 个状态（对应 `type_id`）：

#### State 0: Query（提问）
- **动作**: 自动播放 `Video[0]`（初始提问）
- **用户操作**:
  - 🔵 **听不清/再说一遍** → 转到 State 1
  - 🟢 **回答正确** → 转到 State 2
  - 🟠 **忘记了** → 转到 State 3

#### State 1: Repeat（重复）
- **动作**: 播放 `Video[1]`（温和重复）
- **用户操作**: 同 State 0（可继续回答或再次请求重复）

#### State 2: Correct（正确反馈）
- **动作**: 播放 `Video[2]`（正向鼓励）
- **用户操作**:
  - 🟢 **下一题** → 加载下一个 Question（返回 State 0）
  - 🏠 **返回菜单**（如果是最后一题）

#### State 3: Guide（引导）
- **动作**: 播放 `Video[3]`（引导/安慰）
- **用户操作**:
  - 🔄 **重试** → 重新加载当前 Question（返回 State 0）
  - ⏭️ **跳过** → 加载下一个 Question（返回 State 0）

### 解耦架构：外部文件加载系统

应用采用完全解耦的架构，视频文件不再需要打包进 APK 安装包。用户可以在首次启动时选择手机或电脑上的任意文件夹作为视频源。

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

### 核心依赖
- **Python**: 3.10+
- **GUI 框架**: Flet 0.80.5+（基于 2026 年最新版本）
- **视频组件**: flet-video 0.80.5+
- **构建工具**: uv (依赖管理) + GitHub Actions (CI/CD)

---

## 🎪 动画化欢迎场景与话题选择器

### 欢迎场景设计

欢迎场景采用多层次 Stack 架构，实现了从模糊背景到清晰前景的视觉过渡：

#### 1. 背景层
- **高斯模糊背景**: 使用双层模糊效果，弱模糊层（5px）提供基础背景，强模糊层（30px）在转场时动态增强
- **动态模糊动画**: 转场时通过透明度动画平滑过渡模糊强度
- **16:9 前景卡片**: 居中显示清晰的封面图片，带有圆角和阴影效果

#### 2. 交互元素
- **触觉反馈按钮**: 琥珀金色主题的进入按钮，支持按下/悬停/点击三种状态反馈
- **按钮动画**: 缩放动画、透明度变化和颜色过渡
- **跨平台触觉支持**: 桌面端支持悬停效果，移动端支持点击反馈

#### 3. 转场动画
- **前景扩张**: 前景卡片放大 3 倍覆盖全屏，营造沉浸式过渡
- **按钮淡出**: 进入按钮逐渐淡出，引导用户注意力
- **背景模糊增强**: 转场时背景模糊度动态增强，突出视觉层次

### 弧形话题选择器

#### 1. 布局设计
- **弧线排列**: 话题卡片沿二次函数弧线排列，中心卡片最靠右，上下卡片逐渐向左偏移
- **视觉焦点**: 中心卡片突出显示（缩放 1.1×），边缘卡片透明度降低
- **动态渲染**: 仅渲染可见区域内的卡片，支持无限滚动循环

#### 2. 交互体验
- **垂直拖拽**: 通过 `GestureDetector` 检测垂直拖拽，卡片沿弧线路径平滑移动
- **回弹效果**: 松手后自动对齐到最近的话题卡片
- **受力收缩**: 拖拽时右侧图片略微缩小，松手后回弹，增强物理反馈感

#### 3. 同步动画
- **左右面板同步入场**: 左侧卡片和右侧图片在同一帧内触发动画，避免视觉延迟
- **偏移动画**: 左侧面板从屏幕外滑入，透明度从 0 到 1 同步变化
- **缩放入场**: 右侧图片从小比例 0.9 平滑放大到 1.0

### 两步确认交互

系统实现了三态交互流程，确保用户操作清晰明确：

#### 1. **选择状态** (Selection)
- 中心话题被选中，右侧显示对应封面图片
- 卡片位于弧线标准位置，图片正常显示
- 可拖拽滚动或点击切换话题

#### 2. **聚焦状态** (Focus)
- 点击中心卡片或右侧图片触发
- 中心卡片向右移动并放大（1.3×）
- 右侧图片放大（1.2×），增加视觉焦点
- 此时尚未进入播放，允许用户确认选择

#### 3. **进入状态** (Enter)
- 再次点击已聚焦的元素触发
- 执行 `on_topic_enter` 回调，进入话题播放
- 支持滚动或点击其他位置退出聚焦状态

### 右侧图片预览系统

#### 1. 实时同步
- 右侧图片始终与选中的话题封面同步
- 使用 `AnimatedSwitcher` 实现平滑过渡
- 交叉淡入淡出动画，避免视觉闪烁

#### 2. 状态联动
- 拖拽滚动时图片实时更新
- 聚焦状态下图片配合放大
- 转场时与左侧面板同步入场

### 技术实现要点

#### 1. 数据模型扩展
- `Topic` 类新增 `cover_image_path` 字段
- `data_loader.py` 自动扫描 `cover.jpg` / `cover.png` 文件
- 每个话题文件夹支持封面图片，增强视觉展示

#### 2. 动画性能优化
- 使用隐式动画 (`animate_*` 属性) 而非显式关键帧
- 拖拽时禁用动画 (`anim_duration=0`)，确保跟手性
- 同一帧内批量更新属性，减少重绘次数

#### 3. 跨平台适配
- 触觉反馈系统根据平台特性调整
- 桌面端支持悬停效果，移动端优化点击反馈
- 使用 `clip_behavior=ft.ClipBehavior.NONE` 避免动画裁剪

### 测试与验证

欢迎场景可通过 `test_welcome.py` 独立测试：
```bash
# 运行欢迎场景测试
python test_welcome.py
```

测试脚本加载实际话题数据，验证封面图片加载、动画过渡和交互流程。

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

### 数据结构（已扩展）

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
    cover_image_path: str = "" # 封面图片路径（支持欢迎场景展示）
```

**新增字段说明**:
- `cover_image_path`: 话题封面图片路径，支持 `cover.jpg`、`cover.png`、`cover.jpeg`、`cover.webp` 格式
- **自动扫描**: `data_loader.py` 自动在每个话题文件夹中扫描封面文件
- **视觉增强**: 用于欢迎场景的背景模糊层、前景卡片和右侧图片预览
- **向后兼容**: 如果找不到封面图片，该字段为空字符串，系统有相应降级处理

---

## ⚠️ 故障排除

### 常见问题

#### 1. ModuleNotFoundError（模块导入错误）

**问题描述**:
```
ModuleNotFoundError: No module named 'data_loader'
ModuleNotFoundError: No module named 'config'
```

**原因**:
- 未从项目根目录运行应用
- Python 路径未包含 `src` 目录
- 使用了错误的运行命令

**解决方案**:
```bash
# ✅ 正确：从项目根目录运行
cd /path/to/GongGong
flet run src/main.py

# ✅ 正确：使用 uv 运行
uv run flet run src/main.py

# ❌ 错误：不要在 src 目录内运行
cd src
flet run main.py

# ❌ 错误：不要直接使用 python 运行
python src/main.py
```

#### 2. 视频播放黑屏

**问题描述**:
- 桌面端使用 `ft.AppView.WEB_BROWSER` 模式时视频正常
- 桌面客户端模式和 Android 应用中视频显示黑屏
- 其他功能完全正常

**临时解决方案**:
```python
# 在开发调试时可使用 Web 模式
ft.run(main, assets_dir="assets", view=ft.AppView.WEB_BROWSER)
```

#### 3. Flet 0.80.5 API 变更

**问题描述**:
- Windows PC: `ft.FilePicker` 报 "Unknown control: filepicker"
- Android APK: `flet_permission_handler` 报 "Unknown control: permission_handler"

**解决方案**:
- 已修复：改用 Flet 0.80.5 的内联实例化 API
- FilePicker 和 PermissionHandler 现在都是 Service 类型，不再需要添加到 `page.overlay`

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

## 📝 更新日志

### 2026-02-14: 动画化欢迎场景与弧形话题选择器
- **欢迎场景实现**:
  - 新增 `src/views/welcome.py` 模块，实现完整动画过渡
  - 全屏模糊背景 + 16:9 前景卡片 + 触觉反馈按钮
  - 支持背景模糊动态增强和前景扩张动画
- **弧形卡片选择器**:
  - 话题卡片沿二次函数弧线排列，中心卡片突出显示
  - 支持垂直拖拽滚动和回弹效果，增强物理反馈感
  - 右侧实时图片预览，与左侧卡片同步切换
- **两步确认交互**:
  - 实现选择 → 聚焦 → 进入的三态交互流程
  - 支持滚动或点击其他位置退出聚焦状态
  - 确保用户操作清晰明确，避免误操作
- **数据模型扩展**:
  - `Topic` 类新增 `cover_image_path` 字段
  - `data_loader.py` 自动扫描话题封面图片
  - 支持 `cover.jpg`、`cover.png`、`cover.jpeg`、`cover.webp` 格式
- **同步动画优化**:
  - 左右面板在同一帧内同步入场，避免视觉延迟
  - 拖拽时禁用动画确保跟手性，松手后启用平滑过渡
  - 使用隐式动画 (`animate_*` 属性) 提升性能

### 2026-02-13: 模块化架构重构
- **视图层分解**:
  - 将单一的 `views.py` 分解为 `src/views/` 包
  - 创建独立的 `menu.py`、`setup.py`、`player.py` 模块
  - 提高代码可维护性和团队协作效率
- **导入优化**:
  - 修复所有模块间的导入语句
  - 移除不必要的 `src.` 前缀
  - 确保模块化架构的正确运行方式

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

### 2026-02-04: UI 优化与视频播放器改进
- **全局窗口设置**:
  - 移除页面内边距 (`page.padding = 0`)，实现全沉浸式体验
  - 设置背景色为黑色 (`page.bgcolor = ft.Colors.BLACK`)，提供影院式边框
  - 确保不创建默认的系统应用栏
- **播放器视图重构**:
  - 使用三层 Stack 架构实现沉浸式覆盖
  - 修复菜单隐藏逻辑和双击暂停功能
  - 优化 Android 视频质量和宽高比

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
- 遵循模块化架构设计原则

---

## 📄 许可证

Copyright (C) 2026 GongGong Family

---

## 👤 作者

GongGong Developer  
邮箱: 1641782731@qq.com
