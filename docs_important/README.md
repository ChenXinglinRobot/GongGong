# Flet 文档速查指南 (Flet Documentation Index)

此文件整理了项目中的所有 Flet 相关技术文档，以便 AI 和开发者快速查找相应内容。

## 📂 快速目录导航

| 分类 | 内容描述 | 关键主题 |
| :--- | :--- | :--- |
| **[01_Core_Concepts](./01_Core_Concepts)** | 核心概念与机制 | 路由导航、客户端存储原理 |
| **[02_Controls_and_Services](./02_Controls_and_Services)** | UI 控件与系统服务 | 文件选择、视频播放、权限管理 |
| **[03_Storage_and_Files](./03_Storage_and_Files)** | 文件与持久化存储 | 磁盘读写、SharedPreferences、系统路径 |
| **[04_Build_and_Publish](./04_Build_and_Publish)** | 构建、打包与发布 | flet build/pack、发布指南 |
| **[05_Advanced_Reference](./05_Advanced_Reference)** | 高阶参考资料 | 手势识别、触感反馈、层叠布局 |
| **[06_Layout_and_UI](./06_Layout_and_UI)** | 布局与UI组件 | 扩展控件、布局控制、StackFit与Boxfit |

---

## 🔍 详细文件索引

### 🚀 核心与导航 (Core Concepts)
- [Navigation and Routing](./01_Core_Concepts/Navigation%20and%20Routing.md): 深入理解 Flet 的路由系统与单页应用 (SPA) 架构。
- [Client Storage](./01_Core_Concepts/Client%20Storage.md): 客户端侧的持久化键值对存储概念。

### 🛠️ UI 增强与系统服务 (Controls & Services)
- [FilePicker](./02_Controls_and_Services/FilePicker.md): 原生文件选择器，支持选择、上传与保存。
- [FletVideo](./02_Controls_and_Services/FletVideo.md): 高性能视频播放器集成指南。
- [Permission Handler](./02_Controls_and_Services/Permission%20Handler.md): 跨平台运行时权限管理。
- [Container](./02_Controls_and_Services/Container.md): 容器控件，支持背景色、边框、内边距和对齐方式。
- [Image](./02_Controls_and_Services/Image.md): 图像显示控件。
- [CanvasImage](./02_Controls_and_Services/CanvasImage.md): 画布图像控件。
- [ImageRepeat](./02_Controls_and_Services/ImageRepeat.md): 图像重复模式。
- [Card](./02_Controls_and_Services/Card.md): Material Design卡片控件。
- [ListView](./02_Controls_and_Services/ListView.md): 列表视图控件。

### 💾 数据持久化 (Storage & Files)
- [Read and Write Files](./03_Storage_and_Files/Read%20and%20Write%20Files.md): 使用 Python 标准库进行文件操作。
- [SharedPreferences](./03_Storage_and_Files/SharedPreferences.md): 访问底层的持久化键值存储服务。
- [StoragePaths](./03_Storage_and_Files/StoragePaths.md): 获取应用专属的各类系统路径（缓存、文档等）。

### 📦 打包与分发 (Build & Publish)
- [flet build](./04_Build_and_Publish/flet%20build.md): 官方跨平台构建工具详解。
- [flet pack](./04_Build_and_Publish/flet%20pack.md): 使用 PyInstaller 进行桌面端快速打包。
- [Publishing a Flet app](./04_Build_and_Publish/Publishing%20a%20Flet%20app.md): 全面的发布流程说明。

### 📚 技术参考 (Advanced Reference)
- [GestureDetector](./05_Advanced_Reference/GestureDetector.md): 各类手势（点击、拖拽等）的监听。
- [HapticFeedback](./05_Advanced_Reference/HapticFeedback.md): 移动端震动与触感反馈。
- [Stack](./05_Advanced_Reference/Stack.md): 控件的层叠与定位。
- [Animations](./05_Advanced_Reference/Animations.md): 隐式动画与动画类型。
- [Alignment](./05_Advanced_Reference/Alignment.md): 对齐方式详解。
- [Offset](./05_Advanced_Reference/Offset.md): 偏移量控制。
- [DragUpdateEvent](./05_Advanced_Reference/DragUpdateEvent.md): 拖拽更新事件。

### 🎨 布局与UI组件 (Layout & UI)
- [ExpandingControls](./06_Layout_and_UI/ExpandingControls.md): 扩展控件详解。
- [LayoutControl](./06_Layout_and_UI/LayoutControl.md): 布局控制基础。
- [StackFitAndBoxfit](./06_Layout_and_UI/StackFitAndBoxfit.md): StackFit与Boxfit布局模式。

---
*整理日期: 2026/02/15*
