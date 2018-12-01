from gui.buttons.button import Button
from utils import scene_utils
from utils.gui_utils import Themes
from utils.managers.project_manager import ProjectManager
from utils.string_utils import StringUtils


class CreateButton(Button):

    def __init__(self, pos=0):
        Button.__init__(self, StringUtils.get_string("ID_CREATE"), pos)

    def on_click(self, board, project_info=None, form=None):
        super().on_click(board)
        if project_info is not None:
            ProjectManager.create_project(project_info)
            board.set_scene(scene_utils.DEVELOP_SCENE, project=ProjectManager.get_project_info(
                project_info.get("PROJECT_NAME")))

    def update_button(self, color=Themes.DEFAULT_THEME.get("button")):
        super().update_button(StringUtils.get_string("ID_CREATE"), color)
