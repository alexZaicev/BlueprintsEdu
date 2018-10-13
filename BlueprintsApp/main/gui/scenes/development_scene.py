from gui.scenes.scene_builder import SceneBuilder
from utils import logger_utils

class DevelopmentScene(SceneBuilder):

    def __init__(self, display, theme, project):
        SceneBuilder.__init__(self, display, theme)
        self.__logger = logger_utils.get_logger(__name__)
        self.__project = project

    def draw_scene(self):
        # PREPARE DATA
        # DISPLAY
        self.display.fill(self.theme.get("background"))
        super().draw_scene()

    def check_events(self, event, board):
        super().check_events(event, board)
