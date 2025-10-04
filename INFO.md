
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
