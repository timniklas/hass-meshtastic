from functools import partial

from homeassistant.core import HomeAssistant

import meshtastic
import meshtastic.tcp_interface

class MeshtasticAPI:
    def __init__(self, hass: HomeAssistant):
        self._hass = hass
        self._iface = None
    
    async def connectTCP(self, device_adress: str):
        f_kwargs = {'hostname': device_adress}
        self._iface = await self._hass.async_add_executor_job(
            partial(meshtastic.tcp_interface.TCPInterface, **f_kwargs)
        )
    
    @property
    def nodes(self):
        if self._iface == None:
            return None
        return self._iface.nodes
    
    async def sendText(self, destinationId: str, message: str):
        await self._hass.async_add_executor_job(self._iface.sendText, message, destinationId)
