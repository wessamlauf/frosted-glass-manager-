"""Config flow for Frosted Glass Manager."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.selector import (
    ColorRGBSelector,
    ColorRGBSelectorConfig,
)

from .const import DOMAIN, DEFAULT_LIGHT_RGB, DEFAULT_DARK_RGB

class FrostedGlassConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Frosted Glass Manager."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            return self.async_create_entry(title="Frosted Glass Manager", data={})

        return self.async_show_form(step_id="user")

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return FrostedGlassOptionsFlow(config_entry)


class FrostedGlassOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow (Settings)."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        # Get current values or defaults
        current_light = self.config_entry.options.get("light_primary", DEFAULT_LIGHT_RGB)
        current_dark = self.config_entry.options.get("dark_primary", DEFAULT_DARK_RGB)

        # Schema with Native Color Picker
        schema = vol.Schema({
            vol.Required("light_primary", default=current_light): ColorRGBSelector(
                ColorRGBSelectorConfig()
            ),
            vol.Required("dark_primary", default=current_dark): ColorRGBSelector(
                ColorRGBSelectorConfig()
            ),
        })

        return self.async_show_form(
            step_id="init",
            data_schema=schema,
            description_placeholders=None
        )
