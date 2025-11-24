"""The Frosted Glass Manager integration."""
import logging
import os

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.typing import ConfigType

from .const import (
    DOMAIN, 
    THEME_TEMPLATE, 
    THEME_FILENAME, 
    DEFAULT_LIGHT_RGB, 
    DEFAULT_DARK_RGB,
    DEFAULT_LIGHT_BG,
    DEFAULT_DARK_BG
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
    
    # Získanie farieb
    light_rgb_list = entry.options.get("light_primary", DEFAULT_LIGHT_RGB)
    dark_rgb_list = entry.options.get("dark_primary", DEFAULT_DARK_RGB)
    
    # Získanie pozadí
    light_bg = entry.options.get("light_bg", DEFAULT_LIGHT_BG)
    dark_bg = entry.options.get("dark_bg", DEFAULT_DARK_BG)
    
    # Konverzie
    light_rgb_str = rgb_to_str(light_rgb_list)
    light_hex = rgb_to_hex(light_rgb_list)
    dark_rgb_str = rgb_to_str(dark_rgb_list)
    dark_hex = rgb_to_hex(dark_rgb_list)
    
    _LOGGER.info(f"Updating Theme. Light: {light_hex}, Dark: {dark_hex}")

    # Nahrádzanie v šablóne
    theme_content = THEME_TEMPLATE.replace(
        "__LIGHT_RGB_STR__", light_rgb_str
    ).replace(
        "__LIGHT_HEX__", light_hex
    ).replace(
        "__LIGHT_BG__", light_bg
    ).replace(
        "__DARK_RGB_STR__", dark_rgb_str
    ).replace(
        "__DARK_HEX__", dark_hex
    ).replace(
        "__DARK_BG__", dark_bg
    )
    
    themes_dir = hass.config.path("themes")
    file_path = os.path.join(themes_dir, THEME_FILENAME)
    
    if not os.path.exists(themes_dir):
        os.makedirs(themes_dir)

    def _write_file():
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(theme_content)

    await hass.async_add_executor_job(_write_file)
    await hass.services.async_call("frontend", "reload_themes")
