import asyncio
from pubsub import pub
from functools import partial
from homeassistant.core import HomeAssistant

import meshtastic
import meshtastic.tcp_interface

import logging
_LOGGER = logging.getLogger(__name__)

class MeshtasticAPI:
    def __init__(self, hass: HomeAssistant, async_updateCallback):
        self._hass = hass
        self._iface = None
        self._async_updateCallback = async_updateCallback
        pub.subscribe(self._onDisconnect, "meshtastic.connection.lost")
        pub.subscribe(self._onReceiveUpdate, "meshtastic.receive.position")
        pub.subscribe(self._onReceiveUpdate, "meshtastic.receive.user")
        pub.subscribe(self._onReceiveText, "meshtastic.receive.text")

    @property
    def nodes(self):
        if self._iface == None:
            return None
        return self._iface.nodes

    @property
    def connected(self):
        if self._iface == None or not hasattr(self._iface, 'isConnected'):
            return False
        return self._iface.isConnected
    
    def _onDisconnect(self, interface, topic=pub.AUTO_TOPIC):
        _LOGGER.warn("Lost connection, reconnecting")
        asyncio.run_coroutine_threadsafe(
            self.connect(), self._hass.loop
        ).result()

    def _onReceiveUpdate(self, packet, interface):
        asyncio.run_coroutine_threadsafe(
            self._async_updateCallback(), self._hass.loop
        ).result()

    def _onReceiveText(self, packet, interface):
        self._hass.bus.fire("meshtastic_receive_text", {
            'from': packet['from'],
            'to': packet['to'],
            'message': packet['decoded']['payload'].decode("utf-8")
        })
    
    async def sendText(self, destinationId: str, message: str):
        await self._hass.async_add_executor_job(self._iface.sendText, message, destinationId)

class TCPMeshtasticAPI(MeshtasticAPI):
    def __init__(self, hass: HomeAssistant, async_updateCallback, device_address: str):
        super().__init__(hass, async_updateCallback)
        self._hostname = device_address
    
    async def connect(self):
        #dont connect if already connected
        if self.connected:
            return None
        f_kwargs = {'hostname': self._hostname}
        self._iface = await self._hass.async_add_executor_job(
            partial(meshtastic.tcp_interface.TCPInterface, **f_kwargs)
        )
