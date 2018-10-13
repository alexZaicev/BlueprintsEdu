from gui.buttons.button import Button
from utils.string_utils import StringUtils
from utils import scene_utils


class CreateButton(Button):

    def __init__(self, theme, pos):
        Button.__init__(self, StringUtils.get_string("ID_CREATE"), theme, pos)

    def on_click(self, board):
        board.set_scene(scene_utils.DEVELOP_SCENE)
        super().on_click(board)
