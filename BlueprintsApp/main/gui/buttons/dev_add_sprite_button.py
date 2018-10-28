from gui.buttons.button import Button
from utils.string_utils import StringUtils
from utils.gui_utils import Themes


class DevAddSpriteButton(Button):

    def __init__(self, pos):
        Button.__init__(self, StringUtils.get_string("ID_ADD_SPRITE"), pos)

    def on_click(self, board, form):
        super().on_click(board)
        form.add_sprite()

    def update_button(self, color=Themes.DEFAULT_THEME.get("button")):
        super().update_button(StringUtils.get_string("ID_ADD_SPRITE"), color)
