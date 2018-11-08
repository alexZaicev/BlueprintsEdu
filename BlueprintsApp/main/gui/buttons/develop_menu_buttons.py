from gui.buttons.button import Button
from utils.string_utils import StringUtils
from utils.gui_utils import Themes
from utils.enums import status
from utils import scene_utils


class AddAttrButton(Button):

    def __init__(self, pos=0):
        Button.__init__(self, StringUtils.get_string("ID_ADD_ATTRIBUTE"), pos)

    def on_click(self, board, form=None):
        super().on_click(board)
        form.add_attribute()

    def update_button(self, text=None, color=Themes.DEFAULT_THEME.get("button")):
        if text is None:
            text = StringUtils.get_string("ID_ADD_ATTRIBUTE")
        super().update_button(text, color)


class AddCharacterButton(Button):

    def __init__(self, pos=0):
        Button.__init__(self, StringUtils.get_string("ID_ADD_CHARACTER"), pos)

    def on_click(self, board, form=None):
        super().on_click(board)
        form.add_character()

    def update_button(self, text=None, color=Themes.DEFAULT_THEME.get("button")):
        if text is None:
            text = StringUtils.get_string("ID_ADD_CHARACTER")
        super().update_button(text, color)


class AddFunctionButton(Button):

    def __init__(self, pos=0):
        Button.__init__(self, StringUtils.get_string("ID_ADD_FUNCTION"), pos)

    def on_click(self, board, form=None):
        super().on_click(board)
        form.add_function()

    def update_button(self, text=None, color=Themes.DEFAULT_THEME.get("button")):
        if text is None:
            text = StringUtils.get_string("ID_ADD_FUNCTION")
        super().update_button(text, color)


class AddSpriteButton(Button):

    def __init__(self, pos=0):
        Button.__init__(self, StringUtils.get_string("ID_ADD_SPRITE"), pos)

    def on_click(self, board, form=None):
        super().on_click(board)
        form.add_sprite()

    def update_button(self, text=None, color=Themes.DEFAULT_THEME.get("button")):
        if text is None:
            text = StringUtils.get_string("ID_ADD_SPRITE")
        super().update_button(text, color)


class EditButton(Button):

    def __init__(self, pos=0):
        Button.__init__(self, StringUtils.get_string("ID_EDIT"), pos)

    def on_click(self, board, form=None):
        super().on_click(board)

    def update_button(self, text=None, color=Themes.DEFAULT_THEME.get("button")):
        if text is None:
            text = StringUtils.get_string("ID_EDIT")
        super().update_button(text, color)


class FileButton(Button):

    def __init__(self, pos=0):
        Button.__init__(self, StringUtils.get_string("ID_FILE"), pos)

    def on_click(self, board, form=None):
        super().on_click(board)

    def update_button(self, text=None, color=Themes.DEFAULT_THEME.get("button")):
        if text is None:
            text = StringUtils.get_string("ID_FILE")
        super().update_button(text, color)


class RunButton(Button):

    def __init__(self, pos=0):
        Button.__init__(self, StringUtils.get_string("ID_RUN"), pos)

    def on_click(self, board, form=None):
        super().on_click(board)

    def update_button(self, text=None, color=Themes.DEFAULT_THEME.get("button")):
        if text is None:
            text = StringUtils.get_string("ID_RUN")
        super().update_button(text, color)


class SettingsButton(Button):

    def __init__(self, pos=0):
        Button.__init__(self, StringUtils.get_string("ID_SETTINGS"), pos)

    def on_click(self, board, form=None):
        super().on_click(board)

    def update_button(self, text=None, color=Themes.DEFAULT_THEME.get("button")):
        if text is None:
            text = StringUtils.get_string("ID_SETTINGS")
        super().update_button(text, color)


class SaveButton(Button):

    def __init__(self, pos=0):
        Button.__init__(self, StringUtils.get_string("ID_SAVE"), pos)

    def on_click(self, board, form=None):
        super().on_click(board)
        form.save_project()

    def update_button(self, text=None, color=Themes.DEFAULT_THEME.get("button")):
        if text is None:
            text = StringUtils.get_string("ID_SAVE")
        super().update_button(text, color)


class SaveExitButton(Button):

    def __init__(self, pos=0):
        Button.__init__(self, StringUtils.get_string("ID_SAVE_AND_EXIT"), pos)

    def on_click(self, board, form=None):
        super().on_click(board)
        if form is not None:
            form.save_project()
        board.app_status = status.EXIT

    def update_button(self, text=None, color=Themes.DEFAULT_THEME.get("button")):
        if text is None:
            text = StringUtils.get_string("ID_SAVE_AND_EXIT")
        super().update_button(text, color)


class CloseProject(Button):

    def __init__(self, pos=0):
        Button.__init__(self, StringUtils.get_string("ID_CLOSE_PROJECT"), pos)

    def on_click(self, board, form=None):
        super().on_click(board)
        if form is not None:
            form.save_project()
        board.set_scene(scene_utils.LOAD_SCENE)

    def update_button(self, text, color):
        if text is None:
            text = StringUtils.get_string("ID_CLOSE_PROJECT")
        super().update_button(text, color)


class ClearConnections(Button):

    def __init__(self, pos=0):
        Button.__init__(self, StringUtils.get_string("ID_CLEAR_CONNECTIONS"), pos)

    def update_button(self, text, color):
        if text is None:
            text = StringUtils.get_string("ID_CLEAR_CONNECTIONS")
        super().update_button(text, color)

    def on_click(self, board, form=None):
        super().on_click(board)
        if form is not None:
            form.clear_connections()
