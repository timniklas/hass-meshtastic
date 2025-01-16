from dataclasses import dataclass
from datetime import timedelta

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_ADDRESS, CONF_TYPE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

import meshtastic
import meshtastic.tcp_interface

from .const import DOMAIN

import logging
_LOGGER = logging.getLogger(__name__)

@dataclass
class MeshtasticApiData:
    """Class to hold api data."""

    nodes: dict | None = None

class MeshtasticCoordinator(DataUpdateCoordinator):
    """My coordinator."""

    data: GoveeApiData

    def __init__(self, hass: HomeAssistant, config_entry: ConfigEntry) -> None:
        """Initialize coordinator."""

        # Set variables from values entered in config flow setup
        self.device_address = config_entry.data[CONF_ADDRESS]
        self.device_type = config_entry.data[CONF_TYPE]

        self.connected = False
        
        # Initialise DataUpdateCoordinator
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN} ({config_entry.unique_id})",
            # Set update method to get devices on first load.
            update_method=self._async_update_data,
            # Do not set a polling interval as data will be pushed.
            # You can remove this line but left here for explanatory purposes.
            update_interval=timedelta(seconds=30)
        )

    def _get_data(self):
        match(self.device_type):
          case 'tcp':
            iface = meshtastic.tcp_interface.TCPInterface(hostname=self.device_address)
            self.connected = True
            return MeshtasticApiData(
                nodes=iface.nodes
            )
          case _:
            raise Exception("unknown device type")

    async def _async_push_data(self):
        self.async_set_updated_data(self._get_data())

    async def _async_update_data(self):
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        return self._get_data()
