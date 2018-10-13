from gui.buttons.button import Button
from utils.string_utils import StringUtils
from utils.enums import status

class ExitButton(Button):

    def __init__(self, theme, pos):
        Button.__init__(self, StringUtils.get_string("ID_EXIT"), theme, pos)

    def on_click(self, board):
        board.app_status = status.EXIT
        super().on_click(board)
