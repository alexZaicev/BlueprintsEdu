from utils import logger_utils
import os
import time
import datetime
import shutil
from project import Project
import json
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
            dirs = [directory for directory in os.listdir(ProjectManager.PATH)
                    if os.path.isdir(os.path.join(ProjectManager.PATH, directory)) and
                    ProjectManager.is_valid_project(ProjectManager.PATH + directory)
                    ]
            for directory in dirs:
                t = time.ctime(max(os.path.getmtime(root) for root, _, _ in os.walk(ProjectManager.PATH + directory)))
                result.append(Project(directory, str(datetime.datetime.strptime(
                    t, "%a %b %d %H:%M:%S %Y"))))
        else:
            ProjectManager.LOGGER.info("No saved projects exists")
        return result

    @classmethod
    def get_project_info(cls, project_name):
        api = ""
        bps, bp_conns = None, None
        try:
            fname = "{}{}\{}{}".format(ProjectManager.PATH, project_name, project_name,
                                       ProjectManager.PROJECT_FILE_EXTENSION)
            with open(fname, "r") as file:
                content = json.load(file)
                if project_name == content.get("PROJECT_NAME"):
                    api = content.get("PROJECT_API")
                    bp_conns = content.get("CONNECTIONS")
                    bps = ProjectManager.get_project_files("{}{}".format(ProjectManager.PATH, project_name))
                    ProjectManager.LOGGER.debug(bp_conns)
                    ProjectManager.LOGGER.debug(bps)
                else:
                    ProjectManager.LOGGER.critical(
                        "Failed to load project. Unknown project name [{}]".format(project_name))
                    # TODO close application after critical error
        except OSError as ex:
            ProjectManager.LOGGER.error("Failed to get project files [{}]".format(project_name))
        return {
            "PROJECT_NAME": project_name,
            "PROJECT_API": api,
            "CONNECTIONS": bp_conns,
            "BLUEPRINTS": bps
        }

    @classmethod
    def create_project(cls, data):
        # TODO don't allow to create with already existing project name OR override the existing one
        d = dict()
        d["PROJECT_NAME"] = data.get("PROJECT_NAME")
        d["PROJECT_API"] = data.get("PROJECT_API")
        d["CONNECTIONS"] = list()
        try:
            if not os.path.exists(ProjectManager.PATH):
                ProjectManager.LOGGER.warning("Unable to find projects directory...")
                ProjectManager.LOGGER.info("Creating new projects directory...")
                os.mkdir(ProjectManager.PATH)

            path = "{}{}".format(ProjectManager.PATH, data.get("PROJECT_NAME"))
            if not os.path.exists(path):
                os.mkdir(path)
            else:
                # TODO don`t allow user to continue
                ProjectManager.LOGGER.error(
                    "Cannot override already existing project [{}]".format(data.get("PROJECT_NAME")))

            with open("{}\{}{}".format(path, data.get("PROJECT_NAME"), ProjectManager.PROJECT_FILE_EXTENSION), "w+") as file:
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
        # PROJECT FILE
        r = dict()
        r["PROJECT_NAME"], r["PROJECT_API"] = project_name
        r["CONNECTIONS"] = bp_conns_content

        f_name = "{}{}\{}{}".format(ProjectManager.PATH, project_name[0],
                                    project_name[0], ProjectManager.PROJECT_FILE_EXTENSION)
        with open(f_name, "w+") as f:
            json.dump(r, f)
        # BLUEPRINT DATA
        for k, v in bp_content.items():
            f_name = "{}{}\{}{}".format(ProjectManager.PATH, project_name[0],
                                        k, ProjectManager.BLUEPRINT_FILE_EXTENSION)
            with open(f_name, "w+") as f:
                f.write(v)

    @classmethod
    def delete_project(cls, directory):
        ProjectManager.LOGGER.debug("Directory: " + directory)
        if os.path.isdir(os.path.join(ProjectManager.PATH, directory)):
            shutil.rmtree(ProjectManager.PATH + directory)
            ProjectManager.LOGGER.debug("Directory: " + directory + " deleted")
