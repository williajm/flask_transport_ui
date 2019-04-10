"""
blah
"""
from importlib import resources
import toml


with resources.open_text('config', 'config.toml') as app_config:
    config = toml.load(app_config)
