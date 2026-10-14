"""Climate Control Center."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import (
    DOMAIN,
    CONF_ZONE_HOME,
)

from .storage import CCCStorage
from .climate_manager import ClimateManager
from .coordinator import CCCCoordinator

PLATFORMS = ["sensor"]


async def async_setup(
    hass: HomeAssistant,
    config: dict,
):
    """YAML setup not supported."""
    return True


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
):
    """Set up Climate Control Center."""

    storage = CCCStorage(hass)

    manager = ClimateManager(
        hass,
        storage,
    )

    await manager.async_initialize()

    coordinator = CCCCoordinator(
        hass=hass,
        manager=manager,
        zone_entity=entry.data[
            CONF_ZONE_HOME
        ],
    )

    await coordinator.async_setup()

    hass.data.setdefault(
        DOMAIN,
        {}
    )

    hass.data[DOMAIN][entry.entry_id] = {
        "storage": storage,
        "manager": manager,
        "coordinator": coordinator,
    }

    await hass.config_entries.async_forward_entry_setups(
        entry,
        PLATFORMS,
    )

    return True


async def async_unload_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
):
    """Unload Climate Control Center."""

    unload_ok = await hass.config_entries.async_unload_platforms(
        entry,
        PLATFORMS,
    )

    if unload_ok:
        hass.data[DOMAIN].pop(
            entry.entry_id
        )

    return unload_ok
