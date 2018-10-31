from gui.buttons.button import Button
from utils.string_utils import StringUtils
from utils.gui_utils import Themes


class DevAddAttrButton(Button):

    def __init__(self, pos):
        Button.__init__(self, StringUtils.get_string("ID_ADD_ATTRIBUTE"), pos)

    def on_click(self, board, form):
        super().on_click(board)
        form.add_attribute()

    def update_button(self, color=Themes.DEFAULT_THEME.get("button")):
        super().update_button(StringUtils.get_string("ID_ADD_ATTRIBUTE"), color)


class DevAddCharacterButton(Button):

    def __init__(self, pos):
        Button.__init__(self, StringUtils.get_string("ID_ADD_CHARACTER"), pos)

    def on_click(self, board, form):
        super().on_click(board)
        form.add_character()

    def update_button(self, color=Themes.DEFAULT_THEME.get("button")):
        super().update_button(StringUtils.get_string("ID_ADD_CHARACTER"), color)


class DevAddFunctionButton(Button):

    def __init__(self, pos):
        Button.__init__(self, StringUtils.get_string("ID_ADD_FUNCTION"), pos)

    def on_click(self, board, form):
        super().on_click(board)
        form.add_function()

    def update_button(self, color=Themes.DEFAULT_THEME.get("button")):
        super().update_button(StringUtils.get_string("ID_ADD_FUNCTION"), color)


class DevAddSpriteButton(Button):

    def __init__(self, pos):
        Button.__init__(self, StringUtils.get_string("ID_ADD_SPRITE"), pos)

    def on_click(self, board, form):
        super().on_click(board)
        form.add_sprite()

    def update_button(self, color=Themes.DEFAULT_THEME.get("button")):
        super().update_button(StringUtils.get_string("ID_ADD_SPRITE"), color)


class DevEditButton(Button):

    def __init__(self, pos):
        Button.__init__(self, StringUtils.get_string("ID_EDIT"), pos)

    def on_click(self, event, board):
        super().on_click(event, board)

    def update_button(self, color=Themes.DEFAULT_THEME.get("button")):
        super().update_button(StringUtils.get_string("ID_EDIT"), color)


class DevFileButton(Button):

    def __init__(self, pos):
        Button.__init__(self, StringUtils.get_string("ID_FILE"), pos)

    def on_click(self, event, board):
        super().on_click(event, board)

    def update_button(self, color=Themes.DEFAULT_THEME.get("button")):
        super().update_button(StringUtils.get_string("ID_FILE"), color)


class DevRunButton(Button):

    def __init__(self, pos):
        Button.__init__(self, StringUtils.get_string("ID_RUN"), pos)

    def on_click(self, event, board):
        super().on_click(event, board)

    def update_button(self, color=Themes.DEFAULT_THEME.get("button")):
        super().update_button(StringUtils.get_string("ID_RUN"), color)


class DevSettingsButton(Button):

    def __init__(self, pos):
        Button.__init__(self, StringUtils.get_string("ID_SETTINGS"), pos)

    def on_click(self, event, board):
        super().on_click(event, board)

    def update_button(self, color=Themes.DEFAULT_THEME.get("button")):
        super().update_button(StringUtils.get_string("ID_SETTINGS"), color)
