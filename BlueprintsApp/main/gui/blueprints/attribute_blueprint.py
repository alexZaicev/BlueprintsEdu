from gui.blueprints.blueprint import Blueprint
from utils.string_utils import StringUtils
from blueprints.attribute_blueprint import AttributeBlueprint as AB


class AttributeBlueprint(Blueprint):

    SIZE = [.2, .1]
    BLUEPRINT_COUNT = 1
    DATA_TYPE = {
        "none": "ID_NONE",
        "int": "ID_INTEGER",
        "string": "ID_STRING",
        "char": "ID_CHARACTER",
        "float": "ID_FLOAT"
    }

    def __init__(self, panel):
        Blueprint.__init__(self, panel, "{}_{}".format(StringUtils.get_string(
            "ID_ATTRIBUTE"), AttributeBlueprint.BLUEPRINT_COUNT), AB())
        AttributeBlueprint.BLUEPRINT_COUNT += 1
        self.set_custom_size(AttributeBlueprint.SIZE)
        self.__data_type = AttributeBlueprint.DATA_TYPE.get(self.get_blueprint().get_data_type())
        self.__value = self.get_blueprint().get_value()

    def get_data(self):
        data = super().get_data()
        data[1] = StringUtils.get_string("ID_ATTRIBUTE")
        data[2] = StringUtils.get_string(self.__data_type)
        data[3] = self.__value
        return data

    def set_data(self, index, data):
        super().set_data(index, data)
