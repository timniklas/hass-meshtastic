import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory, UnitOfElectricPotential, PERCENTAGE
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.components.device_tracker import TrackerEntity, TrackerEntityDescription

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
            NodeTracker(coordinator, DeviceInfo(
                identifiers={(DOMAIN, coordinator.device_address, device_id)}
            ), device_id=device_id)
        ])

class NodeTracker(CoordinatorEntity, TrackerEntity):
    
    _attr_has_entity_name = True

    def __init__(self, coordinator: MeshtasticCoordinator, deviceinfo: DeviceInfo, device_id: str) -> None:
        super().__init__(coordinator)
        self.device_info = deviceinfo
        self.translation_key = "node_tracker"
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
        if self._device_id not in self.coordinator.data.nodes:
            return False
        return 'position' in self._node
    
    @property
    def latitude(self):
        if 'latitudeI' not in self._node['position']:
            return None
        return self._node['position']['latitudeI']
    
    @property
    def longitude(self):
        if 'longitudeI' not in self._node['position']:
            return None
        return self._node['position']['longitudeI']
    
    @property
    def source_type(self):
        if 'locationSource' not in self._node['position']:
            return None
        return self._node['position']['locationSource']
