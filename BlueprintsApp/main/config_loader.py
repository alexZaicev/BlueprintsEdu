import os, re
import json
from utils import logger_utils
from utils import app_utils
from utils.gui_utils import Themes
from utils.string_utils import StringUtils


__LOGGER = logger_utils.get_logger(__name__)
__CONFIGS = dict()

CONFIG_FILE_NAME = "app.config"
ROOT_PATH = re.search('(.*)BlueprintsApp', os.path.dirname(os.path.abspath(__file__))).group(1) + "BlueprintsApp\\"
CONFIG_PATH = ROOT_PATH + CONFIG_FILE_NAME
__LOGGER.debug(CONFIG_PATH)

# TODO set loaded configarions
def __set_configurations():
    app_utils.BOARD_WIDTH = __CONFIGS.get("screen")[0]  #SCREEN SETTINGS
    app_utils.BOARD_HEGHT = __CONFIGS.get("screen")[1]
    StringUtils.set_language(__CONFIGS.get("lang"))  #LANGUAGE
    Themes.set_theme(__CONFIGS.get("theme"))    #THEME

# TODO save configurations
def __save_configurations():
    __CONFIGS.clear()
    __CONFIGS["screen"] = [app_utils.BOARD_WIDTH , app_utils.BOARD_HEGHT]
    __CONFIGS["lang"] = StringUtils.DEFAULT_LANGUAGE
    __CONFIGS["theme"] = Themes.DEFAULT_THEME
    # TODO save configs in json format config file


# TODO load configurations
if not os.path.exists(CONFIG_PATH):
    __LOGGER.error("Configuretion file not found... Make sure file is located in the root path")
    raise ImportError("Configuretion file not found... Make sure file is located in the root path")
else:
    with open(CONFIG_PATH, 'r') as json_cfg:
        cfg = json.load(json_cfg)
        # LOADING CONFIGURATIONS
        # TRY to find customed settings
        try:
            __LOGGER.debug("Loading custom configuration settings...")
            __CONFIGS["screen"] = [cfg["CUSTOM"]["SIZE"]["WIDTH"], cfg["CUSTOM"]["SIZE"]["HEIGHT"]]
            __CONFIGS["lang"] = cfg["CUSTOM"]["LANGUAGE"]
            __CONFIGS["theme"] = cfg["CUSTOM"]["THEME"]

        except KeyError as ex:
            __LOGGER.error("Custom configurations not found")
            __LOGGER.debug("Loading default configurations...")
            __CONFIGS["screen"] = [cfg["DEFAULT"]["SIZE"]["WIDTH"], cfg["DEFAULT"]["SIZE"]["HEIGHT"]]
            __CONFIGS["lang"] = cfg["DEFAULT"]["LANGUAGE"]
            __CONFIGS["theme"] = cfg["DEFAULT"]["THEME"]
        __set_configurations()
