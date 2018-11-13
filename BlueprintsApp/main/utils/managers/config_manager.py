import os
import json
from utils import logger_utils
from utils import app_utils
from utils.gui_utils import Themes
from utils.string_utils import StringUtils
from utils.app_utils import DisplaySettings
from utils.managers.manager import Manager


class ConfigManager(Manager):

    LOGGER = logger_utils.get_logger(__name__)
    DEFAULT_CONFIG = {
        "SIZE":
        {
            "WIDTH": 800,
            "HEIGHT": 600
        },
        "LANGUAGE": "ID_ENGLISH",
        "THEME": "ST_1"
    }

    CONFIG_FILE_NAME = "app.config"
    ROOT_PATH = logger_utils.ROOT_PATH + "BlueprintsApp\\"
    CONFIG_PATH = ROOT_PATH + CONFIG_FILE_NAME


    @classmethod
    def set_configurations(cls):
        cfgs = dict()
        if not os.path.exists(ConfigManager.CONFIG_PATH):
            ConfigManager.LOGGER.error("Configuration file not found...")
            ConfigManager.LOGGER.info("Generating default configuration file...")
            ConfigManager.generate_default_configuration()
        with open(ConfigManager.CONFIG_PATH, 'r') as json_cfg:
            cfg = json.load(json_cfg)
            # LOADING CONFIGURATIONS
            # TRY to find custom settings
            try:
                ConfigManager.LOGGER.info("Loading custom configuration settings...")
                cfgs["screen"] = [cfg["CUSTOM"]["SIZE"]["WIDTH"], cfg["CUSTOM"]["SIZE"]["HEIGHT"]]
                cfgs["lang"] = cfg["CUSTOM"]["LANGUAGE"]
                cfgs["theme"] = cfg["CUSTOM"]["THEME"]
            except KeyError as ex:
                ConfigManager.LOGGER.error("Custom configurations not found")
                ConfigManager.LOGGER.info("Loading default configurations...")
                cfgs["screen"] = [cfg["DEFAULT"]["SIZE"]["WIDTH"], cfg["DEFAULT"]["SIZE"]["HEIGHT"]]
                cfgs["lang"] = cfg["DEFAULT"]["LANGUAGE"]
                cfgs["theme"] = cfg["DEFAULT"]["THEME"]
        app_utils.BOARD_WIDTH = cfgs.get("screen")[0]  # SCREEN SETTINGS
        app_utils.BOARD_HEGHT = cfgs.get("screen")[1]
        StringUtils.set_language(cfgs.get("lang"))  # LANGUAGE
        Themes.set_theme(cfgs.get("theme"))  # THEME

    @classmethod
    def generate_default_configuration(cls):
        cfg_dict = dict()
        cfg_dict["DEFAULT"] = ConfigManager.DEFAULT_CONFIG
        with open(ConfigManager.CONFIG_PATH, 'w+') as cfg_file:
            json.dump(cfg_dict, cfg_file)

    @classmethod
    def save_configurations(cls):
        # TODO implement data crypto for security reasons
        cfg_dict = dict()
        cfg_dict["CUSTOM"] = {
            "SIZE": {
                "WIDTH": DisplaySettings.DEFAULT_SCREEN_SIZE[0],
                "HEIGHT": DisplaySettings.DEFAULT_SCREEN_SIZE[1]
            },
            "LANGUAGE": StringUtils.DEFAULT_LANGUAGE,
            "THEME": Themes.get_value(Themes.DEFAULT_THEME)
        }
        cfg_dict["DEFAULT"] = ConfigManager.DEFAULT_CONFIG
        with open(ConfigManager.CONFIG_PATH, 'w+') as cfg_file:
            json.dump(cfg_dict, cfg_file)
