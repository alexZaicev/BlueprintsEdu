from utils.generators.generator import Generator
from utils.enums.status import Status
from utils.managers.template_manager import TemplateManager
from utils import logger_utils
import os


class PythonGenerator(Generator):

    __LOGGER = logger_utils.get_logger(__name__)

    @classmethod
    def generate(cls, project):
        r = Status.SUCCESS
        temps = TemplateManager.get_templates(project.api)
        for k, v in temps.items():
            content = TemplateManager.read_template(v)
            file = k
            PythonGenerator.__LOGGER.debug(content)
            # CHARACTER DATA
            try:
                content, file = PythonGenerator.generate_character(project, content, file)
            except ValueError as ex:
                PythonGenerator.__LOGGER.debug("No character data generated to file [{}]".format(file))
            PythonGenerator.save_generated_content(project.name, file, content)
        return r

    @classmethod
    def generate_character(cls, project, content, file):
        if file == 'custom_character':
            for ch in project.characters:
                file = "{}_character".format(ch.name.lower())
                # CHANGE CHARACTER CLASS
                try:
                    i = content.index(Generator.CHARACTER_CLASS)
                    code = str(ch)
                    content = PythonGenerator.remove_tag((content[:i] + code + content[i:]), Generator.CHARACTER_CLASS)
                except ValueError as ex:
                    pass
                # ATTRIBUTE GENERATION
                for att in ch.attributes:
                    try:
                        i = content.index(Generator.CHARACTER_ATTR)
                        code = "self.{}\n\t".format(str(att).lower())
                        content = PythonGenerator.remove_tag((content[:i] + code + content[i:]),
                                                             Generator.CHARACTER_ATTR)
                    except ValueError as ex:
                        pass
        return content, file

    @classmethod
    def remove_tag(cls, content, tag):
        try:
            i = content.index(tag)
            content = content[:i] + content[i + len(tag):]
        except ValueError as ex:
            PythonGenerator.__LOGGER.debug("No tag found to remove [{}]".format(tag))
        return content

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
