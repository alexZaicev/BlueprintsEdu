from gui.buttons.button import Button
from utils.string_utils import StringUtils
from utils.gui_utils import Themes
from utils.enums.status import Status
from utils import scene_utils
from utils.comms_utils import CommsUtils
from utils import logger_utils
from utils.managers.execution_manager import ExecutionManager
from utils.app_utils import GeneratorError

LOGGER = logger_utils.get_logger(__name__)


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
        if form is not None:
            form.execute_project()

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
        board.app_status = Status.EXIT

    def update_button(self, text=None, color=Themes.DEFAULT_THEME.get("button")):
        if text is None:
            text = StringUtils.get_string("ID_SAVE_AND_EXIT")
        super().update_button(text, color)


class CloseProjectButton(Button):

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


class ClearConnectionsButton(Button):

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


class GenerateButton(Button):

    def __init__(self, pos=0):
        Button.__init__(self, StringUtils.get_string("ID_GENERATE"), pos)

    def update_button(self, text, color):
        if text is None:
            text = StringUtils.get_string("ID_GENERATE")
        super().update_button(text, color)

    def on_click(self, board, form=None):
        super().on_click(board)
        project = form.get_project_dict()
        json_obj = CommsUtils.build_project_model(project.get("PROJECT")[0], project.get("PROJECT")[1],
                                                  project.get("CHARACTERS"), project.get("ATTRIBUTES"),
                                                  project.get("FUNCTIONS"), project.get("SPRITES"))
        all_good = True
        try:
            if form.generated:
                r = CommsUtils.put("/python/project/{}".format(project.get("PROJECT")[0]), json_obj)
                if r.get("STATUS") == Status.SUCCESS:
                    LOGGER.debug("Project content updated")
                else:
                    all_good = False
            else:
                r = CommsUtils.post("/python/project", json_obj)
                if r.get("STATUS") == Status.PROJECT_REGISTERED:
                    # form.generated = True
                    LOGGER.debug("Project registered")
                else:
                    all_good = False

            if all_good:
                r = CommsUtils.get("/python/generate/{}".format(project.get("PROJECT")[0]))
                if r.get("STATUS") == Status.SUCCESS:
                    LOGGER.debug("Code generation successful")
                    r = CommsUtils.download_project(project.get("PROJECT")[0])
                    if r == Status.SUCCESS:
                        LOGGER.debug("Project archive downloaded")
        except Exception:
            raise GeneratorError("Error occurred while trying to generate project")


class GenerateRunButton(Button):

    def __init__(self, pos=0):
        Button.__init__(self, StringUtils.get_string("ID_GENERATE_AND_RUN"), pos)

    def update_button(self, text, color):
        if text is None:
            text = StringUtils.get_string("ID_GENERATE_AND_RUN")
        super().update_button(text, color)

    def on_click(self, board, form=None):
        super().on_click(board)
        project = form.get_project_dict()
        json_obj = CommsUtils.build_project_model(project.get("PROJECT")[0], project.get("PROJECT")[1],
                                                  project.get("CHARACTERS"), project.get("ATTRIBUTES"),
                                                  project.get("FUNCTIONS"), project.get("SPRITES"))
        all_good = True
        try:
            if form.generated:
                r = CommsUtils.put("/python/project/{}".format(project.get("PROJECT")[0]), json_obj)
                if r.get("STATUS") == Status.SUCCESS:
                    LOGGER.debug("Project content updated")
                else:
                    all_good = False
            else:
                r = CommsUtils.post("/python/project", json_obj)
                if r.get("STATUS") == Status.PROJECT_REGISTERED:
                    # form.generated = True
                    LOGGER.debug("Project registered")
                else:
                    all_good = False
            if all_good:
                r = CommsUtils.get("/python/generate/{}".format(project.get("PROJECT")[0]))
                if r.get("STATUS") == Status.SUCCESS:
                    LOGGER.debug("Code generation successful")
                    r = CommsUtils.download_project(project.get("PROJECT")[0])
                    if r == Status.SUCCESS:
                        LOGGER.debug("Project archive downloaded")
                        ExecutionManager.execute_program(project.get("PROJECT")[0], "app")
        except Exception:
            raise GeneratorError("Error occurred while trying to generate project")


