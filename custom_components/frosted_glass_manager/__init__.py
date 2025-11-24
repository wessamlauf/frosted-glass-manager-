"""The Frosted Glass Manager integration."""
import logging
import os

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import (
    DOMAIN, THEME_TEMPLATE, THEME_FILENAME,
    DEFAULT_LIGHT_PRIMARY, DEFAULT_LIGHT_TEXT, DEFAULT_LIGHT_BG,
    DEFAULT_DARK_PRIMARY, DEFAULT_DARK_TEXT, DEFAULT_DARK_BG
)

_LOGGER = logging.getLogger(__name__)

def rgb_to_hex(rgb_list):
    return "#{:02x}{:02x}{:02x}".format(rgb_list[0], rgb_list[1], rgb_list[2])

def rgb_to_str(rgb_list):
    return f"{rgb_list[0]}, {rgb_list[1]}, {rgb_list[2]}"

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    entry.async_on_unload(entry.add_update_listener(update_theme_listener))
    await async_update_theme_file(hass, entry)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    return True

async def update_theme_listener(hass: HomeAssistant, entry: ConfigEntry):
    await async_update_theme_file(hass, entry)

async def async_update_theme_file(hass: HomeAssistant, entry: ConfigEntry):
    
    # RESET LOGIC
    if entry.options.get("reset_defaults", False):
        _LOGGER.info("Resetting Frosted Glass Theme to Defaults")
        new_options = {
            "light_primary": DEFAULT_LIGHT_PRIMARY,
            "light_bg": DEFAULT_LIGHT_BG,
            "dark_primary": DEFAULT_DARK_PRIMARY,
            "dark_bg": DEFAULT_DARK_BG,
            "reset_defaults": False
        }
        hass.config_entries.async_update_entry(entry, options=new_options)
    
    # Load values
    light_p = entry.options.get("light_primary", DEFAULT_LIGHT_PRIMARY)
    light_bg = entry.options.get("light_bg", DEFAULT_LIGHT_BG)
    
    dark_p = entry.options.get("dark_primary", DEFAULT_DARK_PRIMARY)
    dark_bg = entry.options.get("dark_bg", DEFAULT_DARK_BG)
    
    # Text colors are hardcoded to theme defaults as requested
    light_t = DEFAULT_LIGHT_TEXT
    dark_t = DEFAULT_DARK_TEXT
    
    # Convert colors
    lp_str = rgb_to_str(light_p)
    lp_hex = rgb_to_hex(light_p)
    lt_str = rgb_to_str(light_t)
    
    dp_str = rgb_to_str(dark_p)
    dp_hex = rgb_to_hex(dark_p)
    dt_str = rgb_to_str(dark_t)
    
    _LOGGER.info(f"Generating Theme... Light: {lp_hex}, Dark: {dp_hex}")

    # Replace placeholders in template
    theme_content = THEME_TEMPLATE.replace(
        "__LIGHT_PRIMARY_RGB__", lp_str
    ).replace(
        "__LIGHT_PRIMARY_HEX__", lp_hex
    ).replace(
        "__LIGHT_TEXT_RGB__", lt_str
    ).replace(
        "__LIGHT_BG__", light_bg
    ).replace(
        "__DARK_PRIMARY_RGB__", dp_str
    ).replace(
        "__DARK_PRIMARY_HEX__", dp_hex
    ).replace(
        "__DARK_TEXT_RGB__", dt_str
    ).replace(
        "__DARK_BG__", dark_bg
    )
    
    # Write File
    themes_dir = hass.config.path("themes")
    file_path = os.path.join(themes_dir, THEME_FILENAME)
    
    if not os.path.exists(themes_dir):
        os.makedirs(themes_dir)

    def _write_file():
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(theme_content)

    await hass.async_add_executor_job(_write_file)
    await hass.services.async_call("frontend", "reload_themes")
