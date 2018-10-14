from gui.scenes.scene_builder import SceneBuilder
from utils import logger_utils
from utils.gui_utils import Themes


class DevelopmentScene(SceneBuilder):

    def __init__(self, display, project):
        SceneBuilder.__init__(self, display)
        self.__logger = logger_utils.get_logger(__name__)
        self.__project = project
        self.__logger.debug("{} --- {}".format(project[0], project[1]))

    def draw_scene(self):
        # PREPARE DATA
        # DISPLAY
        self.display.fill(Themes.DEFAULT_THEME.get("background"))
        super().draw_scene()

    def check_events(self, event, board):
        super().check_events(event, board)
