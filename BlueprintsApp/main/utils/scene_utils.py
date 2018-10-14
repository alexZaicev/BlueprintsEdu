from gui.scenes.welcome_scene import WelcomeScene
from gui.scenes.load_scene import LoadScene
from gui.scenes.development_scene import DevelopmentScene
from gui.scenes.configuration_scene import ConfigurationScene
from gui.scenes.project_creation_scene import ProjectCreationScene

# SCENE ENUMS
WELCOME_SCENE = "W_S"
LOAD_SCENE = "L_S"
DEVELOP_SCENE = "D_S"
CONFIG_SCENE = "C_S"
PROJECT_CREATION_SCENE = "PC_S"


def get_scene(type, display, project=None):
    if type == WELCOME_SCENE:
        return WelcomeScene(display)
    elif type == LOAD_SCENE:
        return LoadScene(display)
    elif type == DEVELOP_SCENE:
        return DevelopmentScene(display, project)
    elif type == CONFIG_SCENE:
        return ConfigurationScene(display)
    elif type == PROJECT_CREATION_SCENE:
        return ProjectCreationScene(display)
