from __future__ import annotations

from typing import Any
import voluptuous as vol
from functools import partial

import meshtastic
import meshtastic.tcp_interface

from homeassistant.config_entries import ConfigFlow
from homeassistant.const import CONF_ADDRESS, CONF_TYPE
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.selector import selector

from .const import DOMAIN

class MeshtasticConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, formdata):
        return self.async_show_menu(
            step_id="user", menu_options=[
                "tcp"
            ])

    async def async_step_tcp(self, formdata):
        if formdata is not None:
            device_address = formdata[CONF_ADDRESS]
            #try to connect
            f_kwargs = {'hostname': device_address}
            await self.hass.async_add_executor_job(
                partial(meshtastic.tcp_interface.TCPInterface, **f_kwargs)
            )
            #check if unique
            await self.async_set_unique_id(device_address)
            self._abort_if_unique_id_configured()
            #create entity
            return self.async_create_entry(title=f"Meshtastic {device_address}", data={
                CONF_ADDRESS: device_address,
                CONF_TYPE: 'tcp'
            })
    
        return self.async_show_form(
            step_id="tcp", data_schema=vol.Schema({
                vol.Required(CONF_ADDRESS): str
            })
        )
