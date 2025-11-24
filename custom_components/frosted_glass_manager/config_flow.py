"""Config flow for Frosted Glass Manager."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers.selector import (
    ColorRGBSelector,
    ColorRGBSelectorConfig,
    BooleanSelector,
)

from .const import (
    DOMAIN, 
    DEFAULT_LIGHT_PRIMARY, DEFAULT_LIGHT_BG,
    DEFAULT_DARK_PRIMARY, DEFAULT_DARK_BG
)

class FrostedGlassConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Frosted Glass Manager."""
    VERSION = 1

    async def async_step_user(self, user_input=None):
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
    """Handle options flow."""
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current_light_p = self.config_entry.options.get("light_primary", DEFAULT_LIGHT_PRIMARY)
        current_light_bg = self.config_entry.options.get("light_bg", DEFAULT_LIGHT_BG)
        
        current_dark_p = self.config_entry.options.get("dark_primary", DEFAULT_DARK_PRIMARY)
        current_dark_bg = self.config_entry.options.get("dark_bg", DEFAULT_DARK_BG)

        schema = vol.Schema({
            vol.Required("light_primary", default=current_light_p): ColorRGBSelector(ColorRGBSelectorConfig()),
            vol.Required("light_bg", default=current_light_bg): str,
            
            vol.Required("dark_primary", default=current_dark_p): ColorRGBSelector(ColorRGBSelectorConfig()),
            vol.Required("dark_bg", default=current_dark_bg): str,
            
            vol.Optional("reset_defaults", default=False): BooleanSelector(),
        })

        return self.async_show_form(step_id="init", data_schema=schema)
