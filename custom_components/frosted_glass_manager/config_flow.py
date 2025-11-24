"""Config flow for Frosted Glass Manager."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
# We'll use simple strings for now to avoid selector complexity if imports fail, 
# but selectors provide the color picker.
from homeassistant.helpers.selector import (
    ColorRGBSelector,
    ColorRGBSelectorConfig,
)

from .const import DOMAIN, DEFAULT_PRIMARY_COLOR, DEFAULT_ACCENT_COLOR

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
    """Handle options flow."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        current_primary = self.config_entry.options.get("primary_color", DEFAULT_PRIMARY_COLOR)
        current_accent = self.config_entry.options.get("accent_color", DEFAULT_ACCENT_COLOR)

        # Using a text input that expects HEX for simplicity and robustness
        schema = vol.Schema({
            vol.Required("primary_color", default=current_primary): str,
            vol.Required("accent_color", default=current_accent): str,
        })

        return self.async_show_form(
            step_id="init",
            data_schema=schema,
            description_placeholders=None
        )
