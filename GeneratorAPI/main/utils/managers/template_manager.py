from utils.managers.manager import Manager
from utils import logger_utils
import os


class TemplateManager(Manager):
    ROOT_PATH = logger_utils.ROOT_PATH + "GeneratorAPI\\templates\\"

    TEMPLATE_PATHS = {
        "Car Simulator": "{}{}\\".format(ROOT_PATH, "car_simulator")
    }

    TEMPLATE_EXTENSION = ".py.temp"

    __LOGGER = logger_utils.get_logger(__name__)

    @classmethod
    def get_templates(cls, api):
        path = TemplateManager.TEMPLATE_PATHS.get(api)
        r = dict()
        for root, dirs, files in os.walk(path):
            for file in files:
                if file.endswith(TemplateManager.TEMPLATE_EXTENSION):
                    fn = file.split(".")
                    r[fn[0]] = "{}{}".format(path, file)
                    TemplateManager.__LOGGER.debug(file)
        return r

    @classmethod
    def read_template(cls, path):
        con = ""
        with open(path, "r") as file:
            for line in file:
                con += TemplateManager.spaces_to_tabs(line)
        return con

    @classmethod
    def spaces_to_tabs(cls, line):
        s = ""
        i, t = 0, 0
        while i < len(line):
            if i < 0:
                i = 0
            if i < len(line) - 4:
                if line[i] == " " and line[i + 1] == " " and line[i + 2] == " " and line[i + 3] == " ":
                    s += "\t"
                    line = line[i+4:]
                    t += 1
                else:
                    s += line[i]
                    t = 0
            else:
                s += line[i:]
                break
            i += 1 - t
        return s

