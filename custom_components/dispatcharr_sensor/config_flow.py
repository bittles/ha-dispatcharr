"""Config flow for Dispatcharr Sensor integration."""
from __future__ import annotations
import logging
from typing import Any
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.schema_config_entry_flow import (
    SchemaFlowFormStep,
    SchemaOptionsFlowHandler,
)
from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

OPTIONS_SCHEMA = vol.Schema(
    {
        vol.Optional("enable_epg", default=true): bool
    }
)

# Ask for username and password instead of API token
STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required("host"): str,
        vol.Required("port", default=9191): int,
        vol.Required("username"): str,
        vol.Required("password"): str,
        **OPTIONS_SCHEMA.schema,
    }
)

OPTIONS_FLOW = {
    "init": SchemaFlowFormStep(OPTIONS_SCHEMA),
}

class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Dispatcharr Sensor."""

    VERSION = 1

    def async_get_options_flow(config_entry: ConfigEntry) -> SchemaOptionsFlowHandler:
        return SchemaOptionsFlowHandler(config_entry, OPTIONS_FLOW)

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        if user_input is None:
            return self.async_show_form(
                step_id="user", data_schema=STEP_USER_DATA_SCHEMA
            )
        
        return self.async_create_entry(
            title="Dispatcharr",
            data=user_input,
            options={
                enable_epg: user_input["enable_epg"],
                },
            )