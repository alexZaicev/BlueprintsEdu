from gui.buttons.button import Button
from utils.string_utils import StringUtils
from utils import scene_utils
from utils.gui_utils import Themes


class ApplyButton(Button):

    def __init__(self, pos):
        Button.__init__(self, StringUtils.get_string("ID_APPLY"), pos)

    def on_click(self, board):
        board.set_scene(scene_utils.WELCOME_SCENE)
        super().on_click(board)

    def update_button(self, color=Themes.DEFAULT_THEME.get("button")):
        super().update_button(StringUtils.get_string("ID_APPLY"), color)
