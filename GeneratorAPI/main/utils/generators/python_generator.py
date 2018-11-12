from utils.generators.generator import Generator
from utils.enums.status import Status
from utils.managers.template_manager import TemplateManager
from utils import logger_utils
import os


class PythonGenerator(Generator):

    __LOGGER = logger_utils.get_logger(__name__)

    DEFINITIONS = {
        "GENERATOR_OPEN": "<<<",
        "GENERATOR_CLOSE": ">>>",
        "GENERATOR": "generated code",
        "ATTRIBUTE": "variable",
        "FUNCTION": "function",
        "CHARACTER": "class character",
        "SPRITE": "class sprite"
    }

    ATTR_GEN = "{} {} {} {}".format(DEFINITIONS.get("GENERATOR_OPEN"),
                                    DEFINITIONS.get("GENERATOR"),
                                    DEFINITIONS.get("ATTRIBUTE"),
                                    DEFINITIONS.get("GENERATOR_CLOSE"))

    @classmethod
    def generate(cls, project):
        r = Status.SUCCESS
        temps = TemplateManager.get_templates(project.api)
        for k, v in temps.items():
            content = TemplateManager.read_template(v)
            PythonGenerator.__LOGGER.debug(content)
            # CHARACTER DATA
            for char in project.characters:
                for att in char.attributes:
                    try:
                        i = content.index(PythonGenerator.ATTR_GEN)
                        code = str(att) + "\n\t"
                        content = content[:i] + code + content[i:]
                    except ValueError as ex:
                        PythonGenerator.__LOGGER.debug("No attribute generator tag found in file [{}]".format(k))
            try:
                i = content.index(PythonGenerator.ATTR_GEN)
                content = content[:i] + content[i + len(PythonGenerator.ATTR_GEN):]
                PythonGenerator.save_generated_content(project.name, k, content)
            except ValueError as ex:
                pass
        return r

    @classmethod
    def save_generated_content(cls, project_name, file, content):
        path = "{}{}\\".format(TemplateManager.ROOT_PATH, "out")
        if not os.path.exists(path):
            os.mkdir(path)
        path = "{}{}\\".format(path, project_name)
        if not os.path.exists(path):
            os.mkdir(path)
        with open("{}{}.py".format(path, file), "w+") as f:
            f.write(content)
