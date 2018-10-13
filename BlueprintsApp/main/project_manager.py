from utils import logger_utils
import os
import time
import datetime
import shutil
from project import Project


class ProjectManager(object):

    LOGGER = logger_utils.get_logger(__name__)
    PATH = logger_utils.ROOT_PATH + "BlueprintsApp\projects\\"
    PROJECT_FILE_EXTENSION = ".blue"

    def __init__(self):
        object.__init__(self)
        raise TypeError("Cannot instantiate static managers")

    @staticmethod
    def get_projects(theme):
        result = []
        ProjectManager.LOGGER.info("Fetching Existing Projects")
        if not os.path.exists(ProjectManager.PATH):
            try:
                ProjectManager.LOGGER.error("Projects directory not found")
                ProjectManager.LOGGER.info("Creating new projects directory")
                os.makedirs(ProjectManager.PATH)
            except OSError as ex:
                ProjectManager.LOGGER.error("Failed to create projects directory")
        if len(os.listdir(ProjectManager.PATH)) > 0:
            dirs = [dir for dir in os.listdir(ProjectManager.PATH)
                    if os.path.isdir(os.path.join(ProjectManager.PATH, dir)) and
                    ProjectManager.is_valid_project(ProjectManager.PATH + dir)
                    ]
            for dir in dirs:
                t = time.ctime(max(os.path.getmtime(root) for root, _, _ in os.walk(ProjectManager.PATH + dir)))
                result.append(Project(dir, str(datetime.datetime.strptime(t, "%a %b %d %H:%M:%S %Y")), theme))
        else:
            ProjectManager.LOGGER.info("No saved projects exists")
        return result

    @classmethod
    def is_valid_project(cls, dir):
        check = False
        try:
            files = [file for file in os.listdir(dir)
                     if file.endswith(ProjectManager.PROJECT_FILE_EXTENSION)
                     ]
            if len(files) != 1:
                ProjectManager.LOGGER.error("Invalid project found {}".format(dir))
            else:
                check = True
        except OSError as ex:
            ProjectManager.LOGGER.error("Failed to check project directories")
        return check

    @staticmethod
    def get_project_files(directory):
        pass

    @staticmethod
    def delete_project(directory):
        ProjectManager.LOGGER.debug("Directory: " + directory)
        if os.path.isdir(os.path.join(ProjectManager.PATH, directory)):
            shutil.rmtree(ProjectManager.PATH + directory)
            ProjectManager.LOGGER.debug("Directory: " + directory + " deleted")
