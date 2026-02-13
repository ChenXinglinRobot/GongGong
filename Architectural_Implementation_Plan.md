# 🛡️ Architectural_Implementation_Plan.md
## Goal
实现从 "欢迎场景" 到 "话题选择" 的无缝过渡 UI，替换当前的 `menu.py` 简单网格布局，包含背景模糊、前景扩张动画、弧形卡片选择器、右侧图片预览、以及两步确认交互。

## 与现有架构的集成策略
当前项目使用 `page.views` + 路由分发（`main.py` 中的 `route_change`）。新 UI 将：
- 新建 `src/views/welcome.py` 模块，导出 `get_welcome_view(page, topics, on_topic_enter)` 函数
- 在 `main.py` 的 `/` 路由中，用 `get_welcome_view` 替换 `get_menu_view`
- 保留 `menu.py` 作为备用/简单模式
- `player.py`、`setup.py`、`data_loader.py`、`config.py`、`utils.py` 不需要修改

## 数据模型补充
当前 `Topic` 没有封面图片字段。需要扩展：
- 在每个 `topic_xxx/` 文件夹中放置一张 `cover.jpg`（或 `.png`）作为话题封面
- `data_loader.py` 的 `load_topics()` 扫描时自动检测并存入 `Topic.cover_image_path`
- 欢迎场景的背景图使用第一个话题的封面（或指定的 `welcome.jpg`）

---

## 📅 Step 1: Stack 根容器 + 背景模糊层

### 目标
构建 `welcome.py` 的基础层架构：一个全屏 `Stack`，底层是模糊背景图。

### 实现细节

```python
# Layer 0: 模糊背景 — 使用 Container 的 blur 属性
bg_layer = ft.Container(
    expand=True,
    image=ft.DecorationImage(
        src=cover_image_path,   # 话题封面图路径
        fit=ft.BoxFit.COVER,
    ),
    blur=ft.Blur(20, 20, ft.BlurTileMode.CLAMP),  # 高斯模糊
)

# 根 Stack
root_stack = ft.Stack(
    expand=True,
    clip_behavior=ft.ClipBehavior.NONE,  # 重要：允许子控件缩放超出边界
    controls=[bg_layer],  # 后续步骤会往这里追加层
)
```

### ✅ API 确认（来自 docs_important/step1/container.md）
- `Container.blur` 接受 `BlurValue`，即 `ft.Blur(sigma_x, sigma_y, tile_mode)` ✅
- `Container.image` 接受 `DecorationImage` 对象 ✅
- `Stack.clip_behavior` 默认 `HARD_EDGE`，需显式设为 `NONE` 以允许图片放大溢出 ✅

### ⚠️ 风险点
- `Container.image` 的 `src` 参数：对于外部文件路径，需使用 `file:///` URI 格式（复用现有 `utils.get_video_src` 的逻辑，或新建 `utils.get_image_src`）
- 如果封面图不存在，需要 fallback 到纯色背景

---

## 📅 Step 2: 欢迎场景静态布局（前景图 + 进入按钮）

### 目标
在 Stack 上叠加：居中的清晰 16:9 前景图 + "点击进入回忆" 按钮。配置好隐式动画属性，为 Step 3 的过渡做准备。

### 实现细节

```python
# Layer 1: 前景清晰图片（16:9，居中）
foreground_image = ft.Container(
    width=480,          # 初始宽度（16:9 比例）
    height=270,         # 初始高度
    alignment=ft.Alignment.CENTER,
    image=ft.DecorationImage(
        src=cover_image_path,
        fit=ft.BoxFit.COVER,
    ),
    border_radius=12,
    scale=1.0,
    opacity=1.0,
    # 配置隐式动画
    animate_scale=ft.Animation(duration=800, curve=ft.AnimationCurve.EASE_OUT_CUBIC),
    animate_opacity=ft.Animation(duration=600, curve=ft.AnimationCurve.EASE_OUT),
)

# Layer 2: 进入按钮
enter_button = ft.Container(
    content=ft.Text("点击进入回忆 →", size=20, color=ft.Colors.WHITE),
    opacity=1.0,
    animate_opacity=ft.Animation(duration=400, curve=ft.AnimationCurve.EASE_OUT),on_click=trigger_transition,  # Step 3 定义
)
```

### ✅ API 确认（来自 docs_important/step2/）
- `LayoutControl.scale` 接受 `number`（统一缩放）或 `ft.Scale(scale_x, scale_y)` ✅
- `LayoutControl.animate_scale` 接受 `ft.Animation(duration, curve)` ✅
- `LayoutControl.animate_opacity` 同上 ✅
- `ft.AnimationCurve.EASE_OUT_CUBIC` 是有效的曲线枚举 ✅
- `Container.image` + `DecorationImage` 用于显示图片 ✅

### ⚠️ 风险点
- 前景图的初始尺寸需要根据屏幕大小动态计算（可用 `page.width` / `page.height`），硬编码 480×270 仅作为参考
- 可以使用 `Container.on_size_change` 事件来获取实际容器尺寸

---

## 📅 Step 3: 欢迎 → 话题选择的核心过渡动画

### 目标
点击进入按钮后：前景图放大至全屏 + 按钮淡出 → 等待动画完成 → 切换到话题选择 UI。

### 实现细节

```python
async def trigger_transition(e):
    """触发欢迎场景到话题选择的过渡"""
    # A: 前景图放大（scale 从 1.0 → 覆盖全屏的值）
    # 计算缩放比例：屏幕宽度 / 前景图宽度（取较大值）
    scale_x = page.width / foreground_image.width
    scale_y = page.height / foreground_image.height
    target_scale = max(scale_x, scale_y) * 1.1  # 略微超出以确保覆盖
    foreground_image.scale = target_scale

    # B: 按钮淡出
    enter_button.opacity = 0

    page.update()

    # C: 等待最长动画完成（前景图 800ms）
    await asyncio.sleep(0.85)

    # D: 切换到话题选择 UI（同一个 View 内，替换 Stack 内容）
    show_topic_selection()
```

### 关键设计决策
- **不使用路由切换**：整个过渡在同一个 `ft.View` 内完成，通过操作 `Stack.controls` 实现
- **缩放中心**：`Container` 默认从中心缩放（因为 `alignment=ft.Alignment.CENTER`），无需额外配置
- **裁剪控制**：Step 1 已将 `Stack.clip_behavior` 设为 `NONE`

### ✅ API 确认
- `Container.animate_scale` 配合修改 `Container.scale` 触发隐式动画 ✅
- `asyncio.sleep()` 用于等待动画完成 ✅
- `Stack.clip_behavior = ft.ClipBehavior.NONE` 防止放大图片被裁剪 ✅

### ⚠️ 风险点
- 缩放比例计算依赖 `page.width` / `page.height`，首次渲染时可能为 0。解决方案：在 `on_size_change` 回调中缓存尺寸，或使用 `page.window.width`
- `await asyncio.sleep()` 的时长需要与 `animate_scale` 的 `duration` 匹配

---

## 📅 Step 4: 话题选择 UI — 左侧弧形卡片 + 右侧图片（同步入场）

### 目标
过渡动画完成后，同时显示左侧弧形卡片列表和右侧话题预览图。**两者必须同步出现，不允许延迟加载。**

### 4A: 左侧弧形卡片区域

弧形布局的核心思路：用 `Stack` 手动定位每张卡片，通过计算每张卡片的 `left` 和 `top` 值模拟弧线。

```python
def build_card_list(topics, selected_index):
    """构建弧形排列的卡片列表"""
    cards = []
    visible_count = 5  # 同时可见的卡片数
    center = visible_count // 2  # 中心索引

    for i in range(visible_count):
        # 弧形偏移计算：中心卡片最靠右，上下卡片向左偏移
        distance_from_center = abs(i - center)
        arc_offset_x = -(distance_from_center ** 2) * 15  # 二次函数模拟弧线
        
        card = ft.Container(
            content=ft.Text(topics[i].name, size=18, color=ft.Colors.WHITE),
            width=200,
            height=60,
            bgcolor="#44FFFFFF",  # 半透明白色（毛玻璃效果）
            blur=ft.Blur(10, 10),  # 毛玻璃
            border_radius=10,
            padding=10,
            left=50 + arc_offset_x,  # 弧形 X 偏移
            top=i * 80,              # 垂直间距
            scale=1.1 if i == center else 0.95,
            opacity=1.0 if i == center else 0.6,
            # 动画配置
            animate_position=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
            animate_scale=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
            animate_opacity=ft.Animation(300, ft.AnimationCurve.EASE_OUT),
        )
        cards.append(card)
    return cards
```

### 4B: 右侧图片区域

```python
right_image = ft.Container(
    expand=True,
    image=ft.DecorationImage(
        src=topics[0].cover_image_path,
        fit=ft.BoxFit.COVER,
    ),
    border_radius=16,
    opacity=1.0,
    scale=1.0,
    animate_opacity=ft.Animation(400, ft.AnimationCurve.EASE_IN_OUT),
    animate_scale=ft.Animation(400, ft.AnimationCurve.EASE_OUT),
)
```

### 4C: 同步入场动画

```python
def show_topic_selection():
    """从欢迎场景切换到话题选择 UI"""
    # 预备状态：左侧面板在屏幕外，右侧图片透明
    left_panel = ft.Container(
        # ... 包含弧形卡片的 Stack
        offset=ft.Offset(-1, 0),  # 屏幕左侧外（-100% 宽度）
        opacity=0,
        animate_offset=ft.Animation(600, ft.AnimationCurve.EASE_OUT_CUBIC),
        animate_opacity=ft.Animation(600, ft.AnimationCurve.EASE_OUT),
    )
    
    right_panel = ft.Container(
        # ... 包含右侧图片
        opacity=0,
        scale=0.95,
        animate_opacity=ft.Animation(600, ft.AnimationCurve.EASE_OUT),
        animate_scale=ft.Animation(600, ft.AnimationCurve.EASE_OUT),
    )

    # 替换 Stack 内容
    root_stack.controls = [bg_layer, left_panel, right_panel]
    page.update()

    # 🔥 关键：同一帧内同时触发两个面板的入场
    # 不使用 asyncio.sleep 分隔！
    left_panel.offset = ft.Offset(0, 0)
    left_panel.opacity = 1
    right_panel.opacity = 1
    right_panel.scale = 1.0
    page.update()  # 单次 update 确保同帧渲染
```

### ✅ API 确认
- `LayoutControl.offset` 接受 `ft.Offset(x, y)`，单位是控件自身尺寸的比例 ✅
- `LayoutControl.animate_offset` 接受 `ft.Animation(duration, curve)` ✅
- `Container.blur` 用于毛玻璃效果 ✅
- `Stack` 内子控件的 `left`/`top` 用于绝对定位 ✅
- 同一个 `page.update()` 调用内的多个属性变更会在同一帧渲染 ✅

### ⚠️ 风险点
- `offset` 的单位是控件自身尺寸的比例，`Offset(-1, 0)` 表示向左平移一个控件宽度。如果 `left_panel` 没有明确宽度，可能行为不确定。建议给 `left_panel` 设置明确的 `width`
- 弧形布局使用 `Stack` + 绝对定位（`left`/`top`），需要手动计算位置。如果话题数量变化，需要动态调整

### ❌ 原计划问题修正
原计划 Step 4 使用 `await asyncio.sleep(0.1)` 在左右面板之间添加 100ms 延迟，**这违反了 UI Spec 的同步规则**。修正为：在同一个 `page.update()` 中同时触发两者的属性变更。

---

## 📅 Step 5: 垂直拖拽/滚动交互（卡片切换）

### 目标
用户垂直拖拽左侧卡片区域时，卡片沿弧线路径移动，切换选中项，同时右侧图片平滑过渡。

### 实现细节

```python
# 用 GestureDetector 包裹左侧面板
gesture_wrapper = ft.GestureDetector(
    content=left_panel_stack,
    on_vertical_drag_update=handle_drag_update,
    on_vertical_drag_end=handle_drag_end,drag_interval=50,  # 节流 50ms
)

accumulated_delta = 0  # 累积拖拽距离
THRESHOLD = 60         # 切换阈值（像素）

async def handle_drag_update(e: ft.DragUpdateEvent):
    """处理垂直拖拽更新"""
    nonlocal accumulated_delta, selected_index
    
    # 获取垂直拖拽距离
    delta_y = e.local_delta.y  # 或 e.primary_delta
    accumulated_delta += delta_y
    
    if abs(accumulated_delta) >= THRESHOLD:
        direction = -1 if accumulated_delta > 0 else 1  # 下拖 = 上一个，上拖 = 下一个
        new_index = selected_index + direction
        new_index = max(0, min(new_index, len(topics) - 1))
        
        if new_index != selected_index:
            selected_index = new_index
            update_card_positions(selected_index)
            update_right_image(selected_index)
        
        accumulated_delta = 0

async def handle_drag_end(e):
    """拖拽结束，重置累积值"""
    nonlocal accumulated_delta
    accumulated_delta = 0
```

### 右侧图片切换动画

```python
def update_right_image(index):
    """平滑切换右侧图片"""
    # 使用 AnimatedSwitcher 实现交叉淡入淡出
    # 或者：先缩小+淡出旧图，再放大+淡入新图
    right_image.opacity = 0
    right_image.scale = 0.95
    page.update()
    
    # 短暂延迟后更换图片源并淡入
    # 注意：这里需要用 on_animation_end 回调来链式触发
    # 而不是 asyncio.sleep（更精确）
```

更优方案 — 使用 `AnimatedSwitcher`：

```python
right_switcher = ft.AnimatedSwitcher(
    content=ft.Image(src=topics[0].cover_image_path, fit=ft.BoxFit.COVER),
    transition=ft.AnimatedSwitcherTransition.FADE_TRANSITION,
    duration=400,
    switch_in_curve=ft.AnimationCurve.EASE_IN_OUT,
    switch_out_curve=ft.AnimationCurve.EASE_IN_OUT,
)

def update_right_image(index):
    right_switcher.content = ft.Image(
        src=topics[index].cover_image_path,
        fit=ft.BoxFit.COVER,
        key=f"topic_img_{index}",  # key 变化触发切换动画
    )
    page.update()
```

### ✅ API 确认（来自 docs_important/step5/）
- `GestureDetector.on_vertical_drag_update` 回调参数类型为 `DragUpdateEvent` ✅
- `DragUpdateEvent.local_delta` 是 `Offset` 对象，有 `.x` 和 `.y` 属性 ✅
- `DragUpdateEvent.primary_delta` 是 `float`，表示主轴方向的拖拽距离 ✅
- `GestureDetector.drag_interval` 用于节流（毫秒） ✅
- `AnimatedSwitcher` 支持 `FADE_TRANSITION` 和 `SCALE` 过渡 ✅

### ⚠️ 风险点
- `primary_delta` 在 `on_vertical_drag_update` 中代表垂直方向的增量，但文档标注为 `float | None`，需要做空值检查
- 建议优先使用 `e.local_delta.y`，更可靠

---

## 📅 Step 6: 两步确认交互（选择 → 聚焦 → 进入）

### 目标
实现 UI Spec 中的三态交互：Selection → Focus → Enter。

### 状态定义

```python
class CardState:
    SELECTION = "selection"  # 默认：卡片在弧线位置，图片正常显示
    FOCUS = "focus"          # 第一次点击：卡片突出 + 图片放大
    ENTER = "enter"          # 第二次点击：进入播放
```

### 实现细节

```python
current_state = CardState.SELECTION

async def handle_card_click(e):
    """处理卡片或右侧图片的点击"""
    nonlocal current_state
    
    if current_state == CardState.SELECTION:
        # → 进入 Focus 状态
        current_state = CardState.FOCUS
        
        # 卡片：向右移动 + 放大
        center_card.left += 20
        center_card.scale = 1.2
        
        # 右侧图片：放大
        right_image.scale = 1.05
        
        page.update()
    
    elif current_state == CardState.FOCUS:
        # → 进入播放
        current_state = CardState.ENTER
        topic = topics[selected_index]
        await on_topic_enter(topic)  # 回调到 main.py 的路由逻辑

async def handle_scroll_or_other(e):
    """滚动或其他操作时，退出 Focus 状态"""
    nonlocal current_state
    if current_state == CardState.FOCUS:
        current_state = CardState.SELECTION
        # 卡片：回到弧线位置
        center_card.left -= 20
        center_card.scale = 1.1
        # 右侧图片：恢复
        right_image.scale = 1.0
        page.update()
```

### ✅ API 确认
- `animate_position`（`left`/`top` 变化）在 `Stack` 子控件上有效 ✅
- `animate_scale` 配合 `scale` 属性变更触发动画 ✅
- 所有过渡可逆（符合 UI Spec "Exit/Return" 要求） ✅

---

## 📅 Step 7: 集成到路由系统 + data_loader 扩展

### 7A: 扩展 data_loader.py

```python
@dataclass
class Topic:
    id: str
    name: str
    questions: List[Question]
    cover_image_path: str = ""  # 新增：封面图片路径
```

在 `load_topics()` 中扫描 `cover.jpg` / `cover.png`：

```python
# 在 topic_dir 扫描循环中添加
cover_candidates = ["cover.jpg", "cover.png", "cover.jpeg"]
cover_path = ""
for candidate in cover_candidates:
    p = topic_dir / candidate
    if p.exists():
        cover_path = p.as_posix()
        break

# 构建 Topic 时传入
Topic(id=topic_id, name=display_name, questions=valid_questions, cover_image_path=cover_path)
```

### 7B: 修改 main.py 路由

```python
# 在 route_change 的 "/" 路由中
if current_route == "/":
    if topics:
        async def on_topic_enter(topic):
            await page.push_route(f"/play/{topic.id}")
        # 替换 get_menu_view 为 get_welcome_view
        page.views.append(views.get_welcome_view(page, topics, on_topic_enter))else:
        await page.push_route("/setup")
```

### 7C: 更新 views/__init__.py

```python
from views.welcome import get_welcome_view
# 保留原有导出
```

---

## 📊 实施顺序总结

| 步骤 | 内容 | 依赖 | 预估复杂度 |
|------|------|------|-----------|
| Step 1 | Stack + 模糊背景层 | 无 | ⭐ |
| Step 2 | 前景图 + 进入按钮 | Step 1 | ⭐ |
| Step 3 | 扩张过渡动画 | Step 2 | ⭐⭐ |
| Step 4 | 弧形卡片 + 右侧图片（同步入场） | Step 3 | ⭐⭐⭐ |
| Step 5 | 垂直拖拽交互 | Step 4 | ⭐⭐⭐ |
| Step 6 | 两步确认（Focus/Enter） | Step 5 | ⭐⭐ |
| Step 7 | 路由集成 + data_loader 扩展 | Step 1-6 | ⭐⭐ |

### 建议开发顺序
1. **先做 Step 7A**（data_loader 扩展），因为后续所有步骤都需要 `cover_image_path`
2. 然后 Step 1 → 2 → 3（欢迎场景，可独立测试）
3. 然后 Step 4 → 5 → 6（话题选择，可独立测试）
4. 最后 Step 7B/7C（集成）

---

## 🔑 关键 API 速查表（Flet 0.80.5 已验证）

| 功能 | API | 来源文档 |
|------|-----|---------|
| 高斯模糊 | `Container(blur=ft.Blur(sx, sy, tile_mode))` | step1/container.md |
| 背景图片 | `Container(image=ft.DecorationImage(src, fit))` | step1/container.md |
| 层叠布局 | `Stack(controls=[...], clip_behavior=...)` | step1/Stack.md |
| 隐式缩放动画 | `animate_scale=ft.Animation(duration, curve)` + 修改 `scale` | step2/Animations.md |
| 隐式透明度动画 | `animate_opacity=ft.Animation(duration, curve)` + 修改 `opacity` | step2/Animations.md |
| 隐式偏移动画 | `animate_offset=ft.Animation(duration, curve)` + 修改 `offset` | step2/Animations.md |
| 隐式位置动画 | `animate_position=ft.Animation(duration, curve)` + 修改 `left`/`top` | step2/Animations.md |
| 偏移（控件比例） | `offset=ft.Offset(x, y)`，单位为控件自身尺寸比例 | step4/Offset.md |
| 对齐 | `ft.Alignment.CENTER`、`ft.Alignment(x, y)` | step3/Alignment.md |
| 缩放 | `scale=number` 或 `scale=ft.Scale(scale_x, scale_y)` | step2/LayoutControl.md |
| 手势检测 | `GestureDetector(on_vertical_drag_update=..., drag_interval=50)` | step5/GestureDetector.md |
| 拖拽增量 | `DragUpdateEvent.local_delta.y` 或 `.primary_delta` | step5/DragUpdateEvent.md |
| 内容切换动画 | `AnimatedSwitcher(content, transition, duration)` | step2/Animations.md |
| 动画结束回调 | `on_animation_end` 事件，`e.data` 含动画名称 | step2/Animations.md |

---

## ❌ 原计划问题总结与修正

| # | 原计划问题 | 修正方案 |
|---|-----------|---------|
| 1 | Step 4 使用 100ms 延迟分隔左右面板入场 | 改为同一 `page.update()` 同帧触发 |
| 2 | 缺少两步确认交互（Selection → Focus → Enter） | 新增 Step 6 |
| 3 | 缺少弧形卡片布局的具体实现方案 | Step 4A 使用 Stack + 二次函数偏移 |
| 4 | 缺少右侧图片平滑切换方案 | Step 5 使用 AnimatedSwitcher |
| 5 | 未说明如何与现有路由系统集成 | 新增 Step 7 + 集成策略章节 |
| 6 | 未考虑 Topic 缺少封面图片字段 | 新增数据模型补充章节 |
| 7 | Blur API 不确定 | 已确认：`Container(blur=ft.Blur(...))` |
| 8 | Offset 坐标系不确定 | 已确认：单位为控件自身尺寸比例 |
| 9 | DragUpdateEvent 属性不确定 | 已确认：`local_delta.y` 和 `primary_delta` |

---

✅ End of Optimized Implementation Plan
