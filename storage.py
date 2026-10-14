from homeassistant.helpers.storage import Store

STORAGE_VERSION = 1
STORAGE_KEY = "climate_control_center"

class CCCStorage:

    def __init__(self, hass):
        self.store = Store(
            hass,
            STORAGE_VERSION,
            STORAGE_KEY
        )

    async def load(self):
        return await self.store.async_load()

    async def save(self, data):
        await self.store.async_save(data)
