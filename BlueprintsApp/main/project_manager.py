from utils import logger_utils
import os
import time
import datetime
import shutil
from project import Project
from utils.gui_utils import Themes
import json
import xmltodict
import dicttoxml
from blueprint_manager import BlueprintManager


class ProjectManager(object):

    LOGGER = logger_utils.get_logger(__name__)
    PATH = logger_utils.ROOT_PATH + "BlueprintsApp\projects\\"
    PROJECT_FILE_EXTENSION = ".blue"
    BLUEPRINT_FILE_EXTENSION = ".bp"

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
            with open(fname, "r") as file:
                content = json.load(file)
                if project_name == content.get("project_name"):
                    api = content.get("project_api")
                    bps = ProjectManager.get_project_files("{}{}".format(ProjectManager.PATH, project_name))
                    ProjectManager.LOGGER.debug(bps)
                else:
                    ProjectManager.LOGGER.critical(
                        "Failed to load project. Unknown project name [{}]".format(project_name))
                    # TODO close application after critical error
        except OSError as ex:
            ProjectManager.LOGGER.error("Failed to get project files [{}]".format(project_name))
        return (project_name, api)

    @classmethod
    def create_project(cls, project):
        # TODO don't allow to create with already existing project name OR override the existing one

        d = dict()
        d["project_name"] = project[0]
        d["project_api"] = project[1]
        d["connections"] = list()
        try:
            if not os.path.exists(ProjectManager.PATH):
                ProjectManager.LOGGER.error("Unable to find projects directory...")
                ProjectManager.LOGGER.error("Creating new projects directory...")
                os.mkdir(ProjectManager.PATH)

            path = "{}{}".format(ProjectManager.PATH, project[0])
            if not os.path.exists(path):
                os.mkdir(path)
            else:
                # TODO don`t allow user to continue
                ProjectManager.LOGGER.error("Cannot override already existing project [{}]".format(project[0]))

            with open("{}\{}{}".format(path, project[0], ProjectManager.PROJECT_FILE_EXTENSION), "w+") as file:
                json.dump(d, file)
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
        # TODO implement security decoding
        fs = list()
        for root, dirs, files in os.walk(directory):
            for f in files:
                if f.endswith(ProjectManager.BLUEPRINT_FILE_EXTENSION):
                    fs.append("{}\{}".format(directory, f))
        content = list()
        for f in fs:
            with open(f, "r") as c:
                content.append(json.load(c))
        return content

    @classmethod
    def save_project(cls, project_name, bp_data, bp_conns):
        # TODO implement security encoding
        bp_content, bp_conns_content = BlueprintManager.parse_blueprints(bp_data, bp_conns)
        ProjectManager.LOGGER.debug("BP content: {}".format(bp_content))
        ProjectManager.LOGGER.debug("BPS connections: {}".format(bp_conns_content))
        # WRITE BLUEPRINT DATA
        # for key, value in bp_content.items():
        #     fname = "{}{}\{}{}".format(ProjectManager.PATH, project_name, key,
        #                                ProjectManager.BLUEPRINT_FILE_EXTENSION)
        #     with open(fname, "w+") as file:
        #         json.dump(value, file)
        # WRITE CONNECTIONS FILE DATA

    @classmethod
    def delete_project(cls, directory):
        ProjectManager.LOGGER.debug("Directory: " + directory)
        if os.path.isdir(os.path.join(ProjectManager.PATH, directory)):
            shutil.rmtree(ProjectManager.PATH + directory)
            ProjectManager.LOGGER.debug("Directory: " + directory + " deleted")
