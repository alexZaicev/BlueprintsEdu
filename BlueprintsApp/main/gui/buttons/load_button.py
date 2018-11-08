from gui.buttons.button import Button
from utils import scene_utils
from utils.string_utils import StringUtils
from utils.gui_utils import Themes


class LoadButton(Button):

    def __init__(self, pos=0):
        Button.__init__(self, StringUtils.get_string("ID_LOAD_PROJECT"), pos)

    def on_click(self, board, form=None):
        board.set_scene(scene_utils.LOAD_SCENE)
        super().on_click(board)

    def update_button(self, color=Themes.DEFAULT_THEME.get("button")):
        super().update_button(StringUtils.get_string("ID_LOAD_PROJECT"), color)
