# 倒计时(Dao Ji Shi) Home Assistant 集成 

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

一个为 Home Assistant 设计的倒计时集成，可以管理纪念日、节日和重要事件的倒计时。

## 功能特点

- 🎯 **三个核心实体**：
  - 倒计时显示：显示即将到来的事件倒计时
  - 纪念日数据：查看所有纪念日数据
  - 纪念日管理：直接添加/删除纪念日

- 📅 **智能日期处理**：
  - 自动处理闰年
  - 支持农历节日
  - 重要事件优先显示

- 🎨 **中文本地化**：
  - 完全中文化的界面
  - 中文错误提示
  - 本地化配置

- 🔄 **实时更新**：
  - 自动刷新倒计时
  - 数据持久化存储
  - 配置可调整更新频率

## 安装

### 通过 HACS（推荐）

1. 在 HACS 中点击「集成」
2. 点击右上角的三个点，选择「自定义仓库」
3. 添加仓库：`https://github.com/lambilly/dao_ji_shi`
4. 选择分类为「集成」
5. 点击「下载」安装
6. 重启 Home Assistant

### 手动安装

1. 下载 `dao_ji_shi` 文件夹
2. 将其复制到 `custom_components` 目录
3. 重启 Home Assistant

## 配置

1. 在 Home Assistant 中进入「配置」->「集成」
2. 点击「添加集成」
3. 搜索「倒计时」
4. 按照界面提示完成配置

### 配置选项

- **更新间隔**：倒计时数据的更新频率（分钟），默认60分钟

## 使用说明

### 三个实体

安装后会自动创建三个实体：

1. **倒计时** (`sensor.dao_ji_shi_countdown`)
   - 显示当前日期
   - 属性中包含详细的倒计时信息

2. **纪念日数据** (`sensor.dao_ji_shi_anniversary_data`)
   - 显示所有纪念日数据
   - 属性中包含完整的纪念日列表

3. **纪念日管理** (`sensor.dao_ji_shi_anniversary_manager`)
   - 用于添加和删除纪念日
   - 通过设置属性和调用服务来管理

### 添加纪念日

1. 进入「开发者工具」->「状态」
2. 找到 `sensor.dao_ji_shi_anniversary_manager` 实体
3. 设置以下属性：
   - `input_date`: 日期 (格式: YYYY-MM-DD)
   - `input_name`: 事件名称
   - `input_describe`: 事件描述
   - `input_type`: 类型 (normal/important/lunar)
   - `input_show`: 是否显示 (true/false)

4. 调用服务 `sensor.anniversary_manager_add_anniversary`

### 删除纪念日

1. 设置 `delete_date` 属性为要删除的日期
2. 调用服务 `sensor.anniversary_manager_delete_anniversary`

### 在 Lovelace 中显示

```yaml
type: entities
entities:
  - entity: sensor.dao_ji_shi_countdown
    name: 倒计时
  - entity: sensor.dao_ji_shi_anniversary_data
    name: 纪念日数据
  - entity: sensor.dao_ji_shi_anniversary_manager
    name: 纪念日管理
