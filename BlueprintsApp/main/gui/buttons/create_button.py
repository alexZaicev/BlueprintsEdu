from gui.buttons.button import Button
from utils.string_utils import StringUtils
from utils import scene_utils
from project_manager import ProjectManager
from utils.gui_utils import Themes


class CreateButton(Button):

    def __init__(self, pos):
        Button.__init__(self, StringUtils.get_string("ID_CREATE"), pos)

    def on_click(self, board, project_info):
        ProjectManager.create_project(project_info)
        board.set_scene(scene_utils.DEVELOP_SCENE, project=project_info)
        super().on_click(board)

    def update_button(self, color=Themes.DEFAULT_THEME.get("button")):
        super().update_button(StringUtils.get_string("ID_CREATE"), color)
