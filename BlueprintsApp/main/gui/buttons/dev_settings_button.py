from gui.buttons.button import Button
from utils.string_utils import StringUtils


class DevSettingsButton(Button):

    def __init__(self, pos):
        Button.__init__(self, StringUtils.get_string("ID_SETTINGS"), pos)

    def on_click(self, event, board):
        super().on_click(event, board)

    def update_button(self):
        super().update_button(StringUtils.get_string("ID_SETTINGS"))
