from gui.scenes.scene_builder import SceneBuilder
from utils import logger_utils

class ConfigurationScene(SceneBuilder):

    def __init__(self, display, theme):
        SceneBuilder.__init__(self, display, theme)
        self.__logger = logger_utils.get_logger(__name__)

    def draw_scene(self):
        # PREPARE DATA
        # DISPLAY
        self.display.fill(self.theme.get("front_screen"))
        super().draw_scene()

    def check_events(self, event, board):
        super().check_events(event, board)
