from gui.buttons.button import Button
from utils.string_utils import StringUtils


class ConfigThemeButton(Button):

    def __init__(self, pos):
        Button.__init__(self, StringUtils.get_string("ID_THEME"), pos)

    def on_click(self, board):
        super().on_click(board)

    def update_button(self):
        super().update_button(StringUtils.get_string("ID_THEME"))
