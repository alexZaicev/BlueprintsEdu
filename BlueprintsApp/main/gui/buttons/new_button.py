from gui.buttons.button import Button
from utils.string_utils import StringUtils
from utils import scene_utils


class NewButton(Button):

    def __init__(self, pos):
        Button.__init__(self, StringUtils.get_string("ID_NEW_PROJECT"), pos)

    def on_click(self, board):
        board.set_scene(scene_utils.PROJECT_CREATION_SCENE)
        super().on_click(board)
