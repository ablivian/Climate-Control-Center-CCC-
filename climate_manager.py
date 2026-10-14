from .const import MODE_HOME
from datetime import datetime

class ClimateManager:

    def __init__(self, hass, storage):
        self.hass = hass
        self.storage = storage

        self.current_mode = MODE_HOME
        self.previous_mode = MODE_HOME

    async def async_initialize(self):

        data = await self.storage.load()

        if data:
            self.current_mode = data.get(
                "current_mode",
                MODE_HOME
            )

            self.previous_mode = data.get(
                "previous_mode",
                MODE_HOME
            )

    async def set_mode(self, mode):

        self.previous_mode = self.current_mode
        self.current_mode = mode

        await self.storage.save(
            {
                "current_mode": self.current_mode,
                "previous_mode": self.previous_mode,
                "updated": datetime.utcnow().isoformat()
            }
        )

    async def restore_previous_mode(self):
        await self.set_mode(
            self.previous_mode
        )
