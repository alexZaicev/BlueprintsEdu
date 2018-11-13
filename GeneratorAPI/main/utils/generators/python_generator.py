from utils.generators.generator import Generator
from utils.enums.status import Status
from utils.managers.template_manager import TemplateManager
from utils import logger_utils
import os


class PythonGenerator(Generator):
    __LOGGER = logger_utils.get_logger(__name__)

    @classmethod
    def generate(cls, project):
        s = Status.SUCCESS
        temps = TemplateManager.get_templates(project.api)

        # CHARACTER DATA
        file = "custom_character"
        content = TemplateManager.read_template(temps.get(file))
        PythonGenerator.generate_character(project, content)

        # SPRITE DATA

        # SYSTEM SPECIFIC DATA (BOARD)
        file = "board"
        content = TemplateManager.read_template(temps.get(file))
        content = PythonGenerator.generate_board(project, content)
        PythonGenerator.save_generated_content(project.name, file, content)

        # SAVE OTHER FILES THAT DO NOT HAVE GENERATOR TAGS
        for k, v in temps.items():
            content = TemplateManager.read_template(v)
            if Generator.FINDER not in content:
                PythonGenerator.save_generated_content(project.name, k, content)

        return s

    @classmethod
    def generate_board(cls, project, content):
        # DEFINE IMPORTS
        data = ""
        for ch in project.characters:
            data += "from {}_character import {}\n".format(ch.name.lower(), str(ch))
        for sp in project.sprites:
            data += "from {}_sprite import {}\n".format(sp.name.lower(), str(sp))
        content = PythonGenerator.insert_data(content, data, Generator.SYSTEM_IMPORT)
        # DEFINE CHARACTER INITIALIZATION
        data = ""
        for ch in project.characters:
            data += "result.append({}(pos={}, size={}, alive={}))\n\t\t".format(str(ch), ch.pos, ch.size, ch.alive)
        content = PythonGenerator.insert_data(content, data, Generator.SYSTEM_INIT_CHARACTER)
        # DEFINE SPRITE INITIALIZATION
        data = ""
        for sp in project.sprites:
            data += "result.append({}())\n\t\t".format(str(sp))
        content = PythonGenerator.insert_data(content, data, Generator.SYSTEM_INIT_SPRITE)
        return content

    @classmethod
    def generate_character(cls, project, content):
        for ch in project.characters:
            f_content = content
            file = "{}_character".format(ch.name.lower())
            # CHANGE CHARACTER CLASS
            f_content = PythonGenerator.insert_data(f_content, str(ch), Generator.CHARACTER_CLASS)
            # ATTRIBUTE GENERATION
            for att in ch.attributes:
                f_content = PythonGenerator.insert_data(f_content,
                                                        "self.{}\n\t".format(str(att)),
                                                        Generator.CHARACTER_ATTR)
            PythonGenerator.save_generated_content(project.name, file, f_content)

    @classmethod
    def remove_tag(cls, content, tag):
        try:
            i = content.index(tag)
            content = content[:i] + content[i + len(tag):]
        except ValueError as ex:
            PythonGenerator.__LOGGER.debug("No tag found to remove [{}]".format(tag))
        return content

    @classmethod
    def insert_data(cls, content, data, tag):
        try:
            i = content.index(tag)
            content = PythonGenerator.remove_tag((content[:i] + data + content[i:]),
                                                 tag)
        except ValueError as ex:
            pass
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
