from gui.buttons.button import Button
from utils.string_utils import StringUtils
from utils.enums import status


class ExitButton(Button):

    def __init__(self, pos):
        Button.__init__(self, StringUtils.get_string("ID_EXIT"), pos)

    def on_click(self, board):
        board.app_status = status.EXIT
        super().on_click(board)

    def update_button(self):
        super().update_button(StringUtils.get_string("ID_EXIT"))
