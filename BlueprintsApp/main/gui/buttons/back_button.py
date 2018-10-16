from gui.buttons.button import Button
from utils.string_utils import StringUtils
from utils import scene_utils
import time


class BackButton(Button):

    def __init__(self, pos):
        Button.__init__(self, StringUtils.get_string("ID_BACK"), pos)

    def on_click(self, board, scene=None):
        super().on_click(board)
        if scene is None:
            board.set_scene(scene_utils.WELCOME_SCENE)
        else:
            board.set_scene(scene)
