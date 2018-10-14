from utils import logger_utils
import os
import time
import datetime
import shutil
from project import Project
from utils.gui_utils import Themes


class ProjectManager(object):

    LOGGER = logger_utils.get_logger(__name__)
    PATH = logger_utils.ROOT_PATH + "BlueprintsApp\projects\\"
    PROJECT_FILE_EXTENSION = ".blue"

    def __init__(self):
        object.__init__(self)
        raise TypeError("Cannot instantiate static managers")

    @classmethod
    def get_projects(cls):
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
                result.append(Project(dir, str(datetime.datetime.strptime(
                    t, "%a %b %d %H:%M:%S %Y"))))
        else:
            ProjectManager.LOGGER.info("No saved projects exists")
        return result

    @classmethod
    def get_project_info(cls, project_name):
        api = ""
        try:
            fname = "{}{}\{}{}".format(ProjectManager.PATH, project_name, project_name,
                                       ProjectManager.PROJECT_FILE_EXTENSION)
            file = open(fname, "r")
            content = file.readlines()
            for line in content:
                if "PROJECT_API=" in line:
                    api = line[12:-1]
                    ProjectManager.LOGGER.debug(api)
            file.close
        except OSError as ex:
            ProjectManager.LOGGER.error("Failed to get project files [{}]".format(project_name))
        return (project_name, api)

    @classmethod
    def create_project(cls, project):
        try:
            path = "{}{}".format(ProjectManager.PATH, project[0])
            os.mkdir(path)
            file = open("{}\{}{}".format(path, project[0], ProjectManager.PROJECT_FILE_EXTENSION), "w", newline="")
            file.write("PROJECT_NAME={}\r\n".format(project[0]))
            file.write("PROJECT_API={}\r\n".format(project[1]))
            # TODO write additional API details
            file.close()
        except Exception as ex:
            ProjectManager.LOGGER.error("Failed to create project directory [{}]".format(str(ex)))

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

    @classmethod
    def get_project_files(cls, directory):
        pass

    @classmethod
    def delete_project(cls, directory):
        ProjectManager.LOGGER.debug("Directory: " + directory)
        if os.path.isdir(os.path.join(ProjectManager.PATH, directory)):
            shutil.rmtree(ProjectManager.PATH + directory)
            ProjectManager.LOGGER.debug("Directory: " + directory + " deleted")
