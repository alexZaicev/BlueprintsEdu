from gui.buttons.button import Button
from utils.string_utils import StringUtils
from utils import scene_utils

class SelectButton(Button):

    def __init__(self, theme, pos):
        Button.__init__(self, StringUtils.get_string("ID_SELECT"), theme, pos)

    def on_click(self, board, project):
        board.set_scene(scene_utils.DEVELOP_SCENE, project)
        super().on_click(board)
