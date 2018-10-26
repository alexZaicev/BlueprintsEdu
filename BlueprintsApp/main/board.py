from utils import logger_utils
from utils import app_utils
import pygame as pg
from pygame.locals import *
from utils.enums import status
from utils import scene_utils
from utils import gui_utils
from utils.gui_utils import Themes
from config_manager import ConfigManager


class Board(object):

    def __init__(self):
        logger = logger_utils.get_logger(__name__)
        logger.info("Board initialized")
        self.app_status = status.STARTED
        pg.init()
        self.__setup_board()

    def __setup_board(self):
        self.clock = pg.time.Clock()
        self.display = pg.display.set_mode((app_utils.BOARD_WIDTH, app_utils.BOARD_HEGHT))
        # TODO load saved theme from config
        self.__scene_builder = scene_utils.get_scene(scene_utils.WELCOME_SCENE, self.display)
        pg.display.set_caption(app_utils.CAPTION)

    def close(self):
        ConfigManager.save_configurations()
        self.app_status = status.EXIT

    def run(self):
        while self.app_status != status.EXIT:
            for event in pg.event.get():
                self.__scene_builder.check_events(event, self)

            self.__scene_builder.draw_scene()

            pg.display.flip()
            self.clock.tick(app_utils.FPS)
        pg.quit()
        return status.SAVE

    def set_scene(self, scene, project=None):
        self.__scene_builder = scene_utils.get_scene(scene, self.display, project)
