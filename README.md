# 倒计时(Dao Ji Shi) Home Assistant 集成

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

一个为 Home Assistant 设计的倒计时集成，可以管理纪念日、节日和重要事件的倒计时。

---

## ✨ 功能特点

- 🎯 **三个核心实体**  
  - 倒计时显示：显示即将到来的事件倒计时  
  - 纪念日数据：查看所有纪念日数据  
  - 纪念日管理：直接添加/删除纪念日  

- 📅 **智能日期处理**  
  - 自动处理闰年  
  - 支持农历节日  
  - 重要事件优先显示  

- 🎨 **中文本地化**  
  - 完全中文化的界面  
  - 中文错误提示  
  - 本地化配置  

- 🔄 **实时更新**  
  - 自动刷新倒计时  
  - 数据持久化存储  
  - 配置可调整更新频率  

---

## 🧩 安装方式

### ✅ 通过 HACS（推荐）

1. 在 HACS 中点击「集成」  
2. 点击右上角的三个点，选择「自定义仓库」  
3. 添加仓库：  
   ```
   https://github.com/lambilly/dao_ji_shi
   ```
4. 选择分类为「集成」  
5. 点击「下载」安装  
6. 重启 Home Assistant  

### 🛠️ 手动安装

1. 下载 `dao_ji_shi` 文件夹  
2. 将其复制到以下目录：  
   ```
   config/custom_components/
   ```
3. 重启 Home Assistant  

---

## ⚙️ 配置说明

1. 在 Home Assistant 中进入「配置」→「集成」  
2. 点击「添加集成」  
3. 搜索 **倒计时**  
4. 按照界面提示完成配置  

### 配置选项
- **更新间隔**：倒计时数据的更新频率（单位：分钟，默认 60 分钟）  

---

## 📡 使用说明

### 三个实体

1. **倒计时** (`sensor.dao_ji_shi_countdown`)  
   - 显示当前日期  
   - 属性中包含详细的倒计时信息  

2. **纪念日数据** (`sensor.dao_ji_shi_anniversary_data`)  
   - 显示所有纪念日数据  
   - 属性中包含完整的纪念日列表  

3. **纪念日管理** (`sensor.dao_ji_shi_anniversary_manager`)  
   - 用于添加和删除纪念日  
   - 通过设置属性和调用服务来管理  

---

### ➕ 添加纪念日

1. 进入「开发者工具」→「状态」  
2. 找到 `sensor.dao_ji_shi_anniversary_manager` 实体  
3. 设置以下属性：

| 属性名 | 示例值 | 说明 |
|--------|---------|------|
| `input_date` | `2025-03-06` | 日期 (格式: YYYY-MM-DD) |
| `input_name` | `丁丁生日` | 事件名称 |
| `input_describe` | `丁丁生日` | 事件描述 |
| `input_type` | `important` | 类型 (normal / important / lunar) |
| `input_show` | `true` | 是否显示 |

4. 调用服务：  
   ```
   sensor.anniversary_manager_add_anniversary
   ```

---

### ➖ 删除纪念日

1. 设置属性：  
   ```
   delete_date: "2025-03-06"
   ```
2. 调用服务：  
   ```
   sensor.anniversary_manager_delete_anniversary
   ```

---

## 🖥️ 在 Lovelace 中显示

```yaml
type: entities
entities:
  - entity: sensor.dao_ji_shi_countdown
    name: 倒计时
  - entity: sensor.dao_ji_shi_anniversary_data
    name: 纪念日数据
  - entity: sensor.dao_ji_shi_anniversary_manager
    name: 纪念日管理
```

---

## 🗂️ 数据格式

纪念日数据存储在 `anniversary.json` 文件中：

```json
{
  "2025-01-01": {
    "name": "元旦",
    "describe": "元旦",
    "type": "normal",
    "show": true
  }
}
```

---

## 🧰 故障排除

### ❌ 集成无法加载
- 检查 Home Assistant 版本是否符合要求  
- 查看日志文件中的错误信息  

### 📅 纪念日不显示
- 确认 `show` 字段设置为 `true`  
- 检查日期格式是否正确 (YYYY-MM-DD)  

### ⏱️ 倒计时计算错误
- 确认系统时区设置正确  
- 检查日期是否在未来  

### 🪵 启用调试日志
在 `configuration.yaml` 中添加：

```yaml
logger:
  default: info
  logs:
    custom_components.dao_ji_shi: debug
```

---

## 💬 支持与反馈

如果您遇到问题或有功能建议，请：
- 查看 [GitHub Issues](https://github.com/lambilly/dao_ji_shi/issues)
- 或创建新的 Issue，提供详细的错误信息和日志  

---

## 📜 许可证
MIT License  

---

## 🤝 贡献
欢迎提交 **Pull Request** 与 **Issue**！  
由 **lambilly** 开发 ❤️
