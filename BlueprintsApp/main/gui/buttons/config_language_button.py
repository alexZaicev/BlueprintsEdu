from gui.buttons.button import Button
from utils.string_utils import StringUtils


class ConfigLanguageButton(Button):

    def __init__(self, pos):
        Button.__init__(self, StringUtils.get_string("ID_LANGUAGE"), pos)

    def on_click(self, board):
        super().on_click(board)
