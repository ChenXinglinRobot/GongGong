# Flet 0.80.5 "Unknown control" 错误修复总结

## 问题分析

### 根本原因
Flet 0.80.5 的 API 发生了根本性变化：
1. **`FilePicker`** 和 **`PermissionHandler`** 现在都是 `Service` 类型（继承自 `Service`）
2. 它们不再需要添加到 `page.overlay` 中
3. 新的使用模式是**内联实例化 + await**

### 具体问题
1. **Windows PC 上的 FilePicker 问题**：
   - 旧代码：`page.overlay.append(picker)` 导致 "Unknown control: filepicker"
   - "隐形盒子" hack 之所以"有效"，是因为 Container 是合法的可视化控件

2. **Android APK 上的 PermissionHandler 问题**：
   - 旧代码：`page.overlay.append(ph)` 导致 "Unknown control: permission_handler"
   - 问题不是原生库缺失，而是 API 使用方式错误

## 修复方案

### 1. 重写 `main.py`
- 移除了所有 `page.overlay.append()` 相关代码
- 不再创建全局的 `FilePicker` 和 `PermissionHandler` 实例
- 简化了路由逻辑，不再传递这些组件参数

### 2. 重写 `views.py` 中的 `get_setup_view` 函数
- 移除了 `file_picker` 和 `permission_handler` 参数
- 改用 Flet 0.80.5 的内联实例化 API：
  ```python
  # PermissionHandler - 直接实例化使用
  ph = fph.PermissionHandler()
  status = await ph.request(fph.Permission.MANAGE_EXTERNAL_STORAGE)
  
  # FilePicker - 直接实例化使用
  selected_path = await ft.FilePicker().get_directory_path(dialog_title="选择视频文件夹")
  ```

### 3. 验证配置文件
- `pyproject.toml`：依赖配置正确，包含 `flet>=0.80.5`、`flet-video>=0.80.5`、`flet-permission-handler>=0.80.5`
- `.github/workflows/build_apk.yml`：构建配置正确，使用 `uv run flet build apk --verbose`

## 技术细节

### Flet 0.80.5 的新 API 模式
根据官方文档：
1. **FilePicker**：可以内联实例化，直接使用 `await ft.FilePicker().pick_files()` 或 `await ft.FilePicker().get_directory_path()`
2. **PermissionHandler**：可以内联实例化，直接使用 `await ph.request(permission)`

### 为什么旧代码会失败？
- 当执行 `page.overlay.append(picker)` 时，Flet 0.80.5 尝试将 `Service` 对象注册为可视化控件
- Flutter 端找不到对应的 widget 实现，因此报出 "Unknown control" 错误

## 测试结果
- ✅ 代码语法检查通过
- ✅ 移除了所有 `page.overlay.append()` 调用
- ✅ 改用内联实例化 API
- ✅ 配置文件无需改动

## 预期效果
1. **Windows PC**：FilePicker 应该能正常工作，不再需要"隐形盒子" hack
2. **Android APK**：PermissionHandler 应该能正常工作，不再报 "Unknown control" 错误
3. **构建过程**：GitHub Actions 构建应该能成功生成 APK

## 后续建议
1. 运行本地测试验证修复效果
2. 触发 GitHub Actions 构建验证 APK 生成
3. 如果仍有问题，检查 Flet 0.80.5 的特定平台注意事项
