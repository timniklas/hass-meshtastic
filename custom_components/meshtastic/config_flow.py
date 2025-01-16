from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.components.bluetooth import (
    BluetoothServiceInfoBleak,
    async_discovered_service_info,
)
from homeassistant.config_entries import ConfigFlow
from homeassistant.const import CONF_ADDRESS, CONF_TYPE
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.selector import selector

from .const import DOMAIN


class MeshtasticConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> FlowResult:
        return self.async_show_menu(
          step_id="user", menu_options=[
            "tcp"
          ])

    async def async_step_tcp(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        if user_input is not None:
            device_address = user_input[CONF_ADDRESS]
            await self.async_set_unique_id(device_address)
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title=f"Meshtastic {device_address}", data={
                CONF_ADDRESS: address,
                CONF_TYPE: 'tcp'
            })
    
        return self.async_show_form(
            step_id="user", data_schema=vol.Schema({
              vol.Required(CONF_ADDRESS): str
            })
        )
