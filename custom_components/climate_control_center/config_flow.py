from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries

from .const import (
    DOMAIN,
    CONF_ZONE_HOME,
)

class ClimateControlCenterConfigFlow(
    config_entries.ConfigFlow,
    domain=DOMAIN,
):
    VERSION = 1

    async def async_step_user(
        self,
        user_input=None,
    ):
        if user_input is not None:
            return self.async_create_entry(
                title="Climate Control Center",
                data=user_input,
            )

        schema = vol.Schema(
            {
                vol.Required(
                    CONF_ZONE_HOME,
                    default="zone.home",
                ): str,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
        )
