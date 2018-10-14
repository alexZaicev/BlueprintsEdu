from gui.buttons.button import Button
from utils import scene_utils
from utils.string_utils import StringUtils


class LoadButton(Button):

    def __init__(self, pos):
        Button.__init__(self, StringUtils.get_string("ID_LOAD_PROJECT"), pos)

    def on_click(self, board):
        board.set_scene(scene_utils.LOAD_SCENE)
        super().on_click(board)
