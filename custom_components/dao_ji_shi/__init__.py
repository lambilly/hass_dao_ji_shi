"""倒计时集成."""
from __future__ import annotations

import json
import logging
import os
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """设置集成."""
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """通过配置条目设置集成."""
    hass.data.setdefault(DOMAIN, {})
    
    # 注册传感器
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """卸载配置条目."""
    await hass.config_entries.async_unload_platforms(entry, ["sensor"])
    
    if DOMAIN in hass.data:
        if entry.entry_id in hass.data[DOMAIN]:
            hass.data[DOMAIN].pop(entry.entry_id)
        
    return True

def load_anniversary_data(hass: HomeAssistant) -> dict[str, Any]:
    """加载纪念日数据."""
    data_path = os.path.join(os.path.dirname(__file__), "anniversary.json")
    
    try:
        with open(data_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        _LOGGER.warning("纪念日数据文件未找到，创建默认文件")
        default_data = {
            "2025-01-01": {
                "name": "元旦",
                "describe": "元旦",
                "type": "normal",
                "show": True
            }
        }
        save_anniversary_data(hass, default_data)
        return default_data
    except Exception as e:
        _LOGGER.error("加载纪念日数据失败: %s", e)
        return {}

def save_anniversary_data(hass: HomeAssistant, data: dict[str, Any]) -> bool:
    """保存纪念日数据."""
    data_path = os.path.join(os.path.dirname(__file__), "anniversary.json")
    
    try:
        with open(data_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        _LOGGER.error("保存纪念日数据失败: %s", e)
        return False