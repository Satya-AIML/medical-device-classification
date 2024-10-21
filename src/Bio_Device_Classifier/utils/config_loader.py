# src/Bio_Device_Classifier/utils/config_loader.py
import configparser
import os
from pathlib import Path

def load_config(config_file='config.ini'):
    config = configparser.ConfigParser()
    config_path = os.path.join(os.path.dirname(__file__), '..', config_file)
    config.read(config_path)
    return config
