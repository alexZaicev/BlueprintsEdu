from gui.buttons.button import Button
from utils.string_utils import StringUtils
from utils.gui_utils import Themes
from utils.enums import status


class AddAttrButton(Button):

    def __init__(self, pos=0):
        Button.__init__(self, StringUtils.get_string("ID_ADD_ATTRIBUTE"), pos)

    def on_click(self, board, form):
        super().on_click(board)
        form.add_attribute()

    def update_button(self, color=Themes.DEFAULT_THEME.get("button")):
        super().update_button(StringUtils.get_string("ID_ADD_ATTRIBUTE"), color)


class AddCharacterButton(Button):

    def __init__(self, pos=0):
        Button.__init__(self, StringUtils.get_string("ID_ADD_CHARACTER"), pos)

    def on_click(self, board, form):
        super().on_click(board)
        form.add_character()

    def update_button(self, color=Themes.DEFAULT_THEME.get("button")):
        super().update_button(StringUtils.get_string("ID_ADD_CHARACTER"), color)


class AddFunctionButton(Button):

    def __init__(self, pos=0):
        Button.__init__(self, StringUtils.get_string("ID_ADD_FUNCTION"), pos)

    def on_click(self, board, form):
        super().on_click(board)
        form.add_function()

    def update_button(self, color=Themes.DEFAULT_THEME.get("button")):
        super().update_button(StringUtils.get_string("ID_ADD_FUNCTION"), color)


class AddSpriteButton(Button):

    def __init__(self, pos=0):
        Button.__init__(self, StringUtils.get_string("ID_ADD_SPRITE"), pos)

    def on_click(self, board, form):
        super().on_click(board)
        form.add_sprite()

    def update_button(self, color=Themes.DEFAULT_THEME.get("button")):
        super().update_button(StringUtils.get_string("ID_ADD_SPRITE"), color)


class EditButton(Button):

    def __init__(self, pos=0):
        Button.__init__(self, StringUtils.get_string("ID_EDIT"), pos)

    def on_click(self, board):
        super().on_click(board)

    def update_button(self, color=Themes.DEFAULT_THEME.get("button")):
        super().update_button(StringUtils.get_string("ID_EDIT"), color)


class FileButton(Button):

    def __init__(self, pos=0):
        Button.__init__(self, StringUtils.get_string("ID_FILE"), pos)

    def on_click(self, board):
        super().on_click(board)

    def update_button(self, color=Themes.DEFAULT_THEME.get("button")):
        super().update_button(StringUtils.get_string("ID_FILE"), color)


class RunButton(Button):

    def __init__(self, pos=0):
        Button.__init__(self, StringUtils.get_string("ID_RUN"), pos)

    def on_click(self, board):
        super().on_click(board)

    def update_button(self, color=Themes.DEFAULT_THEME.get("button")):
        super().update_button(StringUtils.get_string("ID_RUN"), color)


class SettingsButton(Button):

    def __init__(self, pos=0):
        Button.__init__(self, StringUtils.get_string("ID_SETTINGS"), pos)

    def on_click(self, board):
        super().on_click(board)

    def update_button(self, color=Themes.DEFAULT_THEME.get("button")):
        super().update_button(StringUtils.get_string("ID_SETTINGS"), color)


class SaveButton(Button):

    def __init__(self, pos=0):
        Button.__init__(self, StringUtils.get_string("ID_SAVE"), pos)

    def on_click(self, board, form):
        super().on_click(board)
        form.save_project()

    def update_button(self, color=Themes.DEFAULT_THEME.get("button")):
        super().update_button(StringUtils.get_string("ID_SAVE"), color)


class SaveExitButton(Button):

    def __init__(self, pos=0):
        Button.__init__(self, StringUtils.get_string("ID_SAVE_AND_EXIT"), pos)

    def on_click(self, board, form):
        super().on_click(board)
        form.save_project()
        board.app_status = status.EXIT

    def update_button(self, color=Themes.DEFAULT_THEME.get("button")):
        super().update_button(StringUtils.get_string("ID_SAVE_AND_EXIT"), color)
