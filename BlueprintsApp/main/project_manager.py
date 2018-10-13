from utils import logger_utils
import os, time, datetime, shutil
from project import Project

class ProjectManager(object):

    LOGGER = logger_utils.get_logger(__name__)
    PATH = logger_utils.ROOT_PATH + "BlueprintsApp\projects\\"

    def __init__(self):
        object.__init__(self)
        raise TypeError("Cannot instantiate static managers")

    @staticmethod
    def get_projects(theme):
        ProjectManager.LOGGER.info("Fetching Existing Projects")
        # TODO check if directory is a valid project
        dirs = [ dir for dir in os.listdir(ProjectManager.PATH)
            if os.path.isdir(os.path.join(ProjectManager.PATH, dir))
        ]
        result = []
        for dir in dirs:
            t = time.ctime(max(os.path.getmtime(root) for root,_,_ in os.walk(ProjectManager.PATH + dir)))
            result.append(Project(dir, str(datetime.datetime.strptime(t, "%a %b %d %H:%M:%S %Y")), theme))
        return result

    @staticmethod
    def get_project_files(directory):
        pass

    @staticmethod
    def delete_project(directory):
        ProjectManager.LOGGER.debug("Directory: " + directory)
        if os.path.isdir(os.path.join(ProjectManager.PATH, directory)):
            shutil.rmtree(ProjectManager.PATH + directory)
            ProjectManager.LOGGER.debug("Directory: " + directory + " deleted")
