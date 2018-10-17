from utils.string_utils import StringUtils
from gui.buttons.button import Button
from utils import scene_utils


class ConfigurationButton(Button):

    def __init__(self, pos):
        Button.__init__(self, StringUtils.get_string("ID_CONFIGURATION"), pos)

    def on_click(self, board):
        board.set_scene(scene_utils.CONFIG_SCENE)
        super().on_click(board)

    def update_button(self):
        super().update_button(StringUtils.get_string("ID_CONFIGURATION"))
