from configparser import ConfigParser
import os
import sys

def resource_path(relative_path):
    """ Get absolute path to resource (compatible with PyInstaller .exe) """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.abspath(relative_path)

def read_configuration(category, key):
    config = ConfigParser()
    config_path = resource_path(os.path.join("configurations", "config.ini"))
    print(f"🔍 Loading config from: {config_path}")  # KEEP this line for debug
    config.read(config_path)
    return config.get(category, key)