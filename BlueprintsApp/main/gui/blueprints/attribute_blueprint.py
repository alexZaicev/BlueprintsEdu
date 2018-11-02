from gui.blueprints.blueprint import Blueprint
from utils.string_utils import StringUtils
from blueprints.attribute_blueprint import AttributeBlueprint as AB
from utils import logger_utils


class AttributeBlueprint(Blueprint):

    SIZE = [.2, .1]
    DATA_TYPE = {
        "none": "ID_NONE",
        "int": "ID_INTEGER",
        "string": "ID_STRING",
        "char": "ID_CHARACTER",
        "float": "ID_FLOAT"
    }

    def __init__(self, panel):
        Blueprint.__init__(self, panel, AB())
        self.__logger = logger_utils.get_logger(__name__)
        self.set_custom_size(AttributeBlueprint.SIZE)
        self.data_type_pressed = [False, None]  # IS PRESSED; TEXT BOX
        self.data_type_selection = list()

    def reset_selection(self):
        super().reset_selection()
        self.data_type_pressed = [False, None]
        self.data_type_selection = list()

    def initialize(self, coords, size, blueprint, panel):
        super().initialize(coords, size, blueprint, panel)
        # TODO add additional data

    def get_data(self):
        data = super().get_data()
        data[1] = StringUtils.get_string("ID_ATTRIBUTE")
        data[2] = StringUtils.get_string(AttributeBlueprint.DATA_TYPE.get(self.get_blueprint().get_data_type()))
        data[3] = self.get_blueprint().get_value()
        return data

    def set_data(self, index, data):
        if index == 2:
            for key, value in AttributeBlueprint.DATA_TYPE.items():
                if data == StringUtils.get_string(value):
                    self.get_blueprint().set_data_type(key)
        elif index == 3:
            self.get_blueprint().set_value(data)
        super().set_data(index, data)
