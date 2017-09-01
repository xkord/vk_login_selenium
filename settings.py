import os
import copy
import inspect
import logging
from os.path import isabs

logger = logging.getLogger(__name__)

DEFAULT_CONFIG = {}

def read_settings(path=None):
    if path:
        local_settings = get_settings_from_file(path)
        process_settings(local_settings)
    return local_settings

def process_settings(settings):
    """Check settings"""
    settings_to_check = ["LOGIN", "PASSWORD"]
    for name in settings_to_check:
        try:
            settings[name]
        except Exception as e:
            logger.critical('Please set the %s', e)
            exit(0)
    settings

try:
    # SourceFileLoader is the recommended way in 3.3+
    from importlib.machinery import SourceFileLoader

    def load_source(name, path):
        return SourceFileLoader(name, path).load_module()
except ImportError:
    # but it does not exist in 3.2-, so fall back to imp
    import imp
    load_source = imp.load_source

def get_settings_from_module(module=None, default_settings=DEFAULT_CONFIG):
    """Loads settings from a module, returns a dictionary."""

    context = copy.deepcopy(default_settings)
    if module is not None:
        context.update(
            (k, v) for k, v in inspect.getmembers(module) if k.isupper())
    return context

def get_settings_from_file(path, default_settings=DEFAULT_CONFIG):
    """Loads settings from a file path, returning a dict."""
    
    name, ext = os.path.splitext(os.path.basename(path))
    module = load_source(name, path)
    return get_settings_from_module(module, default_settings=default_settings)
