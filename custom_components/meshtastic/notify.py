import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory, UnitOfElectricPotential, PERCENTAGE
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.components.notify import NotifyEntity

from .const import DOMAIN
from .coordinator import MeshtasticCoordinator

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Set up the Sensors."""
    # This gets the data update coordinator from hass.data as specified in your __init__.py
    coordinator: MeshtasticCoordinator = hass.data[DOMAIN][
        config_entry.entry_id
    ].coordinator

    nodes = coordinator.data.nodes
    for device_id in nodes:
        #ignore invalid ids
        if len(device_id) != 9:
            continue

        async_add_entities([
            NotifyNode(coordinator, DeviceInfo(
                identifiers={(DOMAIN, coordinator.device_address, device_id)}
            ), device_id=device_id)
        ])

class NotifyNode(CoordinatorEntity, NotifyEntity):
    
    _attr_has_entity_name = True

    def __init__(self, coordinator: MeshtasticCoordinator, deviceinfo: DeviceInfo, device_id: str) -> None:
        super().__init__(coordinator)
        self.device_info = deviceinfo
        self.translation_key = "notify_node"
        self.unique_id = f"{coordinator.device_address}_{device_id}_{self.translation_key}"
        self._device_id = device_id

    @callback
    def _handle_coordinator_update(self) -> None:
        self.async_write_ha_state()
    
    @property
    def _node(self):
        return self.coordinator.data.nodes[self._device_id]
    
    @property
    def available(self):
        return self._device_id in self.coordinator.data.nodes

    async def async_send_message(self, message: str, title: str | None = None) -> None:
        """Send a message."""
        msg = message
        if title is not None:
            msg = f"{title}: {message}"
        await self.coordinator.sendText(self._device_id, msg)
