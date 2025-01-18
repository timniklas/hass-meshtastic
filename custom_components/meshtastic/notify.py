import logging

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory, UnitOfElectricPotential, PERCENTAGE
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

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
        node = nodes[device_id]
        if 'user' not in node:
            continue
        hwModel = None
        if 'hwModel' in node['user']:
            hwModel = node['user']['hwModel']
        if 'macaddr' in node['user']:
            macaddr = node['user']['macaddr']
        if 'longName' in node['user']:
            longName = node['user']['longName']
        if 'shortName' in node['user']:
            shortName = node['user']['shortName']

        async_add_entities([
            MetricsSensor(coordinator, DeviceInfo(
                #only generate device once!
                name=f"{shortName}_{longName}",
                manufacturer="Meshtastic",
                model=hwModel,
                serial_number=macaddr,
                identifiers={(DOMAIN, coordinator.device_address, device_id)}
            ), device_id=device_id, data_key="batteryLevel", translation="battery", device_class=SensorDeviceClass.BATTERY, unit=PERCENTAGE),
            MetricsSensor(coordinator, DeviceInfo(
                identifiers={(DOMAIN, coordinator.device_address, device_id)}
            ), device_id=device_id, data_key="voltage", translation="voltage", device_class=SensorDeviceClass.VOLTAGE, category=EntityCategory.DIAGNOSTIC, unit=UnitOfElectricPotential.VOLT),
            MetricsSensor(coordinator, DeviceInfo(
                identifiers={(DOMAIN, coordinator.device_address, device_id)}
            ), device_id=device_id, data_key="channelUtilization", translation="channel_utilization", category=EntityCategory.DIAGNOSTIC, unit=PERCENTAGE, visible=False),
            MetricsSensor(coordinator, DeviceInfo(
                identifiers={(DOMAIN, coordinator.device_address, device_id)}
            ), device_id=device_id, data_key="airUtilTx", translation="airtx", category=EntityCategory.DIAGNOSTIC, unit=PERCENTAGE, visible=False)
        ])

class MetricsSensor(CoordinatorEntity):
    
    _attr_has_entity_name = True

    def __init__(self,
    coordinator: MeshtasticCoordinator,
    deviceinfo: DeviceInfo,
    device_id: str,
    data_key: str,
    translation: str,
    unit: str = None,
    device_class: str = None,
    category: str = None,
    visible: bool = True) -> None:
        super().__init__(coordinator)
        self.device_info = deviceinfo
        self.translation_key = translation
        self.unique_id = f"{coordinator.device_address}_{device_id}_{self.translation_key}"
        self.entity_registry_enabled_default = visible
        self._device_id = device_id
        self._data_key = data_key
        if unit is not None:
            self._attr_unit_of_measurement = unit
        if device_class is not None:
            self._attr_device_class = device_class
        if category is not None:
            self._attr_entity_category = category

    @callback
    def _handle_coordinator_update(self) -> None:
        self.async_write_ha_state()

    @property
    def _node(self):
        return self.coordinator.data.nodes[self._device_id]
    
    @property
    def available(self):
        return 'deviceMetrics' in self._node
    
    @property
    def state(self):
        if self._data_key not in self._node['deviceMetrics']:
            return None
        return self._node['deviceMetrics'][self._data_key]
