# 倒计时集成 (Dao Ji Shi)

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

数据格式
纪念日数据存储在 anniversary.json 文件中：

json
{
  "2025-01-01": {
    "name": "元旦",
    "describe": "元旦",
    "type": "normal",
    "show": true
  }
}
故障排除
常见问题
集成无法加载

检查 Home Assistant 版本是否符合要求

查看日志文件中的错误信息

纪念日不显示

确认 show 字段设置为 true

检查日期格式是否正确 (YYYY-MM-DD)

倒计时计算错误

确认系统时区设置正确

检查日期是否在未来

日志
在 configuration.yaml 中启用调试日志：

yaml
logger:
  default: info
  logs:
    custom_components.dao_ji_shi: debug
支持
如果您遇到问题或有建议，请：

查看 GitHub Issues

创建新的 Issue

提供详细的错误信息和日志

许可证
MIT License

贡献
欢迎提交 Pull Request 和 Issue！

text

## 3. INFO.md
```markdown
## 倒计时集成

一个简单易用的倒计时集成，帮助您跟踪重要的纪念日、节日和事件。

### 主要功能

- **智能倒计时显示**：自动计算距离重要事件的剩余天数
- **事件分类管理**：支持普通事件、重要事件和农历节日
- **直观的操作界面**：直接在 Home Assistant 界面中添加和管理事件
- **数据持久化**：所有数据安全存储在本地文件中

### 实体说明

#### 1. 倒计时传感器
- **实体ID**: `sensor.dao_ji_shi_countdown`
- **功能**: 显示即将到来的事件倒计时
- **属性**:
  - `title`: 标题
  - `simple_n`: 简单文本格式（换行）
  - `detail_n`: 详细文本格式（换行）
  - `simple_b`: 简单HTML格式（<br>）
  - `detail_b`: 详细HTML格式（<br>）
  - `update_time`: 更新时间

#### 2. 纪念日数据传感器
- **实体ID**: `sensor.dao_ji_shi_anniversary_data`
- **功能**: 查看所有纪念日数据
- **属性**:
  - `anniversary_data`: 原始纪念日数据
  - `anniversary_list`: 排序后的纪念日列表
  - `data_count`: 纪念日数量

#### 3. 纪念日管理传感器
- **实体ID**: `sensor.dao_ji_shi_anniversary_manager`
- **功能**: 添加和删除纪念日
- **属性**:
  - `input_date`: 输入日期
  - `input_name`: 输入名称
  - `input_describe`: 输入描述
  - `input_type`: 输入类型
  - `input_show`: 是否显示
  - `delete_date`: 要删除的日期
  - 帮助信息和使用说明

### 事件类型说明

- **normal**: 普通事件（默认）
- **important**: 重要事件（会优先显示）
- **lunar**: 农历节日

### 使用示例

#### 添加生日纪念日
```yaml
# 设置输入属性
service: sensor.set_attribute
target:
  entity_id: sensor.dao_ji_shi_anniversary_manager
data:
  input_date: "2025-03-06"
  input_name: "丁丁生日"
  input_describe: "丁丁生日"
  input_type: "important"
  input_show: true

# 添加纪念日
service: sensor.anniversary_manager_add_anniversary
target:
  entity_id: sensor.dao_ji_shi_anniversary_manager
删除纪念日
yaml
# 设置要删除的日期
service: sensor.set_attribute
target:
  entity_id: sensor.dao_ji_shi_anniversary_manager
data:
  delete_date: "2025-03-06"

# 删除纪念日
service: sensor.anniversary_manager_delete_anniversary
target:
  entity_id: sensor.dao_ji_shi_anniversary_manager
自动化示例
每日提醒
yaml
alias: "每日倒计时提醒"
description: "每天早上8点发送倒计时提醒"
trigger:
  - platform: time
    at: "08:00:00"
condition: []
action:
  - service: notify.mobile_app_你的手机
    data:
      message: "{{ state_attr('sensor.dao_ji_shi_countdown', 'simple_n') }}"
重要事件前一天提醒
yaml
alias: "重要事件提醒"
description: "重要事件前一天提醒"
trigger:
  - platform: state
    entity_id: sensor.dao_ji_shi_countdown
condition:
  - condition: template
    value_template: >
      {{ '重要' in state_attr('sensor.dao_ji_shi_countdown', 'simple_n') 
         and '还有1天' in state_attr('sensor.dao_ji_shi_countdown', 'simple_n') }}
action:
  - service: notify.mobile_app_你的手机
    data:
      title: "明天有重要事件！"
      message: "{{ state_attr('sensor.dao_ji_shi_countdown', 'simple_n') }}"
自定义视图
在 Lovelace 中创建专门的倒计时面板：

yaml
type: vertical-stack
cards:
  - type: markdown
    content: |
      # 📅 倒计时
      {{ states('sensor.dao_ji_shi_countdown') }}
  - type: entities
    entities:
      - entity: sensor.dao_ji_shi_countdown
        secondary_info: last-changed
  - type: markdown
    content: |
      ## 今日提醒
      {{ state_attr('sensor.dao_ji_shi_countdown', 'simple_b') | replace('<br>', '\n\n') }}
技术要求
Home Assistant 版本: 2023.8.0 或更高

安装方式: HACS 或手动安装

依赖: 无外部依赖

数据存储: 本地 JSON 文件

更新日志
v1.0.0
初始版本发布

三个核心实体

中文本地化支持

纪念日管理功能

支持与反馈
如果您在使用过程中遇到任何问题，或者有功能建议，请通过 GitHub Issues 联系我们。

由 lambilly 开发
