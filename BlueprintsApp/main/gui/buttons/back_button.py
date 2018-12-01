from gui.buttons.button import Button
from utils import scene_utils
from utils.gui_utils import Themes
from utils.string_utils import StringUtils


class BackButton(Button):

    def __init__(self, pos=0):
        Button.__init__(self, StringUtils.get_string("ID_BACK"), pos)

    def on_click(self, board, scene=None, form=None):
        super().on_click(board)
        if scene is None:
            board.set_scene(scene_utils.WELCOME_SCENE)
        else:
            board.set_scene(scene)

    def update_button(self, color=Themes.DEFAULT_THEME.get("button")):
        super().update_button(StringUtils.get_string("ID_BACK"), color)
