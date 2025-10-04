"""倒计时传感器."""
from __future__ import annotations

import json
import logging
from datetime import datetime, timedelta
from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """设置传感器平台."""
    update_interval = timedelta(
        minutes=entry.options.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL)
    )

    coordinator = DaoJiShiCoordinator(hass, update_interval)
    
    await coordinator.async_config_entry_first_refresh()

    # 存储协调器以便其他实体使用
    hass.data[DOMAIN][entry.entry_id] = coordinator

    sensors = [
        CountdownSensor(coordinator, entry),
        AnniversaryDataSensor(coordinator, entry),
        AnniversaryManagerSensor(coordinator, entry)
    ]
    
    async_add_entities(sensors)

class DaoJiShiCoordinator(DataUpdateCoordinator):
    """数据更新协调器."""

    def __init__(self, hass: HomeAssistant, update_interval: timedelta) -> None:
        """初始化."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=update_interval,
        )
        self.anniversary_data = {}

    async def _async_update_data(self) -> dict[str, Any]:
        """更新数据."""
        try:
            self.anniversary_data = await self.hass.async_add_executor_job(
                load_anniversary_data, self.hass
            )
            return self.calculate_countdowns()
        except Exception as err:
            raise UpdateFailed(f"更新数据错误: {err}") from err

    def calculate_countdowns(self) -> dict[str, Any]:
        """计算倒计时."""
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        current_year = today.year
        
        def is_leap_year(year):
            return (year % 4 == 0 and year % 100 != 0) or year % 400 == 0
        
        results = []
        
        for date_str, event in self.anniversary_data.items():
            if not event.get("show", True):
                continue
            
            date_parts = date_str.split('-')
            if len(date_parts) != 3:
                continue
                
            year = int(date_parts[0])
            month = int(date_parts[1]) - 1
            day = int(date_parts[2])
            
            # 处理2月29日
            if month == 1 and day == 29:
                check_year = year if year > current_year else current_year
                if not is_leap_year(check_year):
                    continue
            
            # 创建目标日期
            if year > current_year:
                target_date = datetime(year, month + 1, day)
            else:
                target_date = datetime(current_year, month + 1, day)
            
            target_date = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
            
            # 验证日期有效性
            if (target_date.year != (year if year > current_year else current_year) or
                target_date.month != month + 1 or
                target_date.day != day):
                continue
                
            if target_date < today:
                continue
                
            diff_days = (target_date - today).days
            
            results.append({
                "name": event["name"],
                "describe": event["describe"],
                "days": diff_days,
                "month": target_date.month,
                "day": target_date.day,
                "timestamp": target_date.timestamp(),
                "type": event.get("type", "normal"),
                "show": event.get("show", True)
            })
        
        # 排序
        results.sort(key=lambda x: x["timestamp"])
        
        # 构建输出
        output_name = []
        output_describe = []
        
        today_event = next((event for event in results if event["days"] == 0), None)
        next_normal_event = next((event for event in results if event["days"] > 0 and event["type"] != "important"), None)
        important_events = [event for event in results if event["type"] == "important" and event["days"] > 0]
        
        title = "【📅倒计时】"
        
        if today_event:
            output_name.append(f"🌻今天是{today_event['describe']}")
            output_describe.append(f"🌻今天是{today_event['describe']}")
        
        for event in important_events:
            output_name.append(f"📙距{event['month']}月{event['day']}日{event['name']}还有{event['days']}天")
            output_describe.append(f"📙距{event['month']}月{event['day']}日{event['describe']}还有{event['days']}天")
        
        if next_normal_event:
            output_name.append(f"📆距{next_normal_event['month']}月{next_normal_event['day']}日{next_normal_event['name']}还有{next_normal_event['days']}天")
            output_describe.append(f"📆距{next_normal_event['month']}月{next_normal_event['day']}日{next_normal_event['describe']}还有{next_normal_event['days']}天")
        
        return {
            "title": title,
            "simple_n": "\n".join(output_name),
            "detail_n": "\n".join(output_describe),
            "simple_b": "<br>".join(output_name),
            "detail_b": "<br>".join(output_describe),
            "date": today.strftime("%Y-%m-%d"),
            "anniversary_data": self.anniversary_data
        }

    async def add_anniversary(self, date: str, name: str, describe: str, 
                            event_type: str = "normal", show: bool = True) -> bool:
        """添加纪念日."""
        # 验证日期格式
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            _LOGGER.error("日期格式错误，应为 YYYY-MM-DD: %s", date)
            return False

        # 更新数据
        self.anniversary_data[date] = {
            "name": name,
            "describe": describe,
            "type": event_type,
            "show": show
        }

        # 保存到文件
        success = await self.hass.async_add_executor_job(
            save_anniversary_data, self.hass, self.anniversary_data
        )

        if success:
            _LOGGER.info("成功添加纪念日: %s - %s", date, name)
            await self.async_refresh()
            return True
        else:
            _LOGGER.error("保存纪念日数据失败")
            return False

    async def delete_anniversary(self, date: str) -> bool:
        """删除纪念日."""
        if date in self.anniversary_data:
            del self.anniversary_data[date]
            
            # 保存到文件
            success = await self.hass.async_add_executor_job(
                save_anniversary_data, self.hass, self.anniversary_data
            )

            if success:
                _LOGGER.info("成功删除纪念日: %s", date)
                await self.async_refresh()
                return True
            else:
                _LOGGER.error("保存纪念日数据失败")
                return False
        else:
            _LOGGER.warning("未找到要删除的纪念日: %s", date)
            return False

class CountdownSensor(SensorEntity):
    """倒计时传感器."""

    def __init__(self, coordinator: DaoJiShiCoordinator, entry: ConfigEntry) -> None:
        """初始化传感器."""
        self.coordinator = coordinator
        self._entry = entry
        self._attr_name = "倒计时"
        self._attr_unique_id = f"{entry.entry_id}_countdown"
        self._attr_icon = "mdi:calendar-clock-outline"

    @property
    def state(self) -> str:
        """返回传感器状态."""
        return self.coordinator.data["date"]

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """返回额外属性."""
        data = self.coordinator.data
        return {
            "title": data["title"],
            "simple_n": data["simple_n"],
            "detail_n": data["detail_n"],
            "simple_b": data["simple_b"],
            "detail_b": data["detail_b"],
            "update_time": data["date"]
        }

    async def async_update(self) -> None:
        """更新传感器."""
        await self.coordinator.async_request_refresh()

class AnniversaryDataSensor(SensorEntity):
    """纪念日数据传感器."""

    def __init__(self, coordinator: DaoJiShiCoordinator, entry: ConfigEntry) -> None:
        """初始化传感器."""
        self.coordinator = coordinator
        self._entry = entry
        self._attr_name = "纪念日数据"
        self._attr_unique_id = f"{entry.entry_id}_anniversary_data"
        self._attr_icon = "mdi:calendar-text"

    @property
    def state(self) -> str:
        """返回传感器状态."""
        return "已加载"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """返回纪念日数据."""
        anniversary_data = self.coordinator.data.get("anniversary_data", {})
        anniversary_list = []
        
        for date, event in anniversary_data.items():
            anniversary_list.append({
                "date": date,
                "name": event.get("name", ""),
                "describe": event.get("describe", ""),
                "type": event.get("type", "normal"),
                "show": event.get("show", True)
            })
        
        # 按日期排序
        anniversary_list.sort(key=lambda x: x["date"])
        
        return {
            "anniversary_data": anniversary_data,
            "anniversary_list": anniversary_list,
            "data_count": len(anniversary_data)
        }

    async def async_update(self) -> None:
        """更新传感器."""
        await self.coordinator.async_request_refresh()

class AnniversaryManagerSensor(SensorEntity):
    """纪念日管理传感器."""

    def __init__(self, coordinator: DaoJiShiCoordinator, entry: ConfigEntry) -> None:
        """初始化传感器."""
        self.coordinator = coordinator
        self._entry = entry
        self._attr_name = "纪念日管理"
        self._attr_unique_id = f"{entry.entry_id}_anniversary_manager"
        self._attr_icon = "mdi:calendar-edit"
        
        # 输入属性
        self._input_date = ""
        self._input_name = ""
        self._input_describe = ""
        self._input_type = "normal"
        self._input_show = True
        self._delete_date = ""
        self._last_action = ""
        self._last_action_status = ""

    @property
    def state(self) -> str:
        """返回传感器状态."""
        return "就绪" if not self._last_action else f"{self._last_action}: {self._last_action_status}"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """返回管理属性和帮助信息."""
        return {
            # 输入字段
            "input_date": self._input_date,
            "input_name": self._input_name,
            "input_describe": self._input_describe,
            "input_type": self._input_type,
            "input_show": self._input_show,
            "delete_date": self._delete_date,
            
            # 状态信息
            "last_action": self._last_action,
            "last_action_status": self._last_action_status,
            
            # 帮助信息
            "date_format": "YYYY-MM-DD",
            "type_options": ["normal", "important", "lunar"],
            "help_add": "设置input_*属性后调用add_anniversary服务添加纪念日",
            "help_delete": "设置delete_date属性后调用delete_anniversary服务删除纪念日"
        }

    async def async_add_anniversary(self) -> None:
        """添加纪念日."""
        if not all([self._input_date, self._input_name, self._input_describe]):
            self._last_action = "添加纪念日"
            self._last_action_status = "失败：缺少必要字段"
            self.async_write_ha_state()
            return

        success = await self.coordinator.add_anniversary(
            self._input_date, 
            self._input_name, 
            self._input_describe,
            self._input_type,
            self._input_show
        )
        
        self._last_action = "添加纪念日"
        self._last_action_status = "成功" if success else "失败"
        
        # 清空输入字段
        if success:
            self._input_date = ""
            self._input_name = ""
            self._input_describe = ""
            self._input_type = "normal"
            self._input_show = True
        
        self.async_write_ha_state()

    async def async_delete_anniversary(self) -> None:
        """删除纪念日."""
        if not self._delete_date:
            self._last_action = "删除纪念日"
            self._last_action_status = "失败：未指定要删除的日期"
            self.async_write_ha_state()
            return

        success = await self.coordinator.delete_anniversary(self._delete_date)
        
        self._last_action = "删除纪念日"
        self._last_action_status = "成功" if success else "失败"
        self._delete_date = ""  # 清空删除日期
        self.async_write_ha_state()

    async def async_set_attribute(self, **kwargs) -> None:
        """设置管理属性."""
        if "input_date" in kwargs:
            self._input_date = kwargs["input_date"]
        if "input_name" in kwargs:
            self._input_name = kwargs["input_name"]
        if "input_describe" in kwargs:
            self._input_describe = kwargs["input_describe"]
        if "input_type" in kwargs:
            self._input_type = kwargs["input_type"]
        if "input_show" in kwargs:
            self._input_show = kwargs["input_show"]
        if "delete_date" in kwargs:
            self._delete_date = kwargs["delete_date"]
        
        self.async_write_ha_state()

def load_anniversary_data(hass: HomeAssistant) -> dict[str, Any]:
    """加载纪念日数据."""
    from . import load_anniversary_data as load_data
    return load_data(hass)

def save_anniversary_data(hass: HomeAssistant, data: dict[str, Any]) -> bool:
    """保存纪念日数据."""
    from . import save_anniversary_data as save_data
    return save_data(hass, data)