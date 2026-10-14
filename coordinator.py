from homeassistant.helpers.update_coordinator import (
    DataUpdateCoordinator
)

from homeassistant.helpers.event import (
    async_track_state_change_event
)

from .const import (
    MODE_AWAY,
    MODE_HOME
)

class CCCCoordinator(
    DataUpdateCoordinator
):

    def __init__(
        self,
        hass,
        manager,
        zone_entity
    ):
        super().__init__(
            hass,
            logger=None,
            name="CCC"
        )

        self.manager = manager
        self.zone_entity = zone_entity

    async def async_setup(self):

        async_track_state_change_event(
            self.hass,
            [self.zone_entity],
            self._zone_changed
        )

    async def _zone_changed(
        self,
        event
    ):
        new_state = event.data.get(
            "new_state"
        )

        if not new_state:
            return

        try:
            count = int(float(new_state.state))
        except ValueError:
            return

        if count == 0:
            await self.manager.set_mode(
                MODE_AWAY
            )

        elif (
            count > 0
            and self.manager.current_mode
            == MODE_AWAY
        ):
            await self.manager.restore_previous_mode()
