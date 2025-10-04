"""配置流."""
from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, OptionsFlow, ConfigEntry
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult

from .const import DOMAIN, CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL

class DaoJiShiConfigFlow(ConfigFlow, domain=DOMAIN):
    """处理配置流."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """处理用户步骤."""
        if user_input is not None:
            return self.async_create_entry(title="倒计时", data=user_input)

        data_schema = vol.Schema({
            vol.Optional(
                CONF_UPDATE_INTERVAL,
                default=DEFAULT_UPDATE_INTERVAL,
            ): int
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            description_placeholders={
                "domain": DOMAIN
            }
        )

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: ConfigEntry,
    ) -> OptionsFlow:
        """获取选项流."""
        return DaoJiShiOptionsFlow(config_entry)

class DaoJiShiOptionsFlow(OptionsFlow):
    """处理选项流."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        """初始化选项流."""
        self.config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """管理选项."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        data_schema = vol.Schema({
            vol.Optional(
                CONF_UPDATE_INTERVAL,
                default=self.config_entry.options.get(
                    CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL
                ),
            ): vol.All(vol.Coerce(int), vol.Range(min=1, max=1440))
        })

        return self.async_show_form(
            step_id="init",
            data_schema=data_schema
        )