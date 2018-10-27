from gui.blueprints.blueprint import Blueprint
from utils.string_utils import StringUtils


class AttributeBlueprint(Blueprint):

    SIZE = [.2, .1]

    def __init__(self, panel, blueprint):
        Blueprint.__init__(self, panel, "Attribute_1", blueprint)
        # TODO improve random blueprint name generation
        self.set_custom_size(AttributeBlueprint.SIZE)

    def get_data(self):
        data = super().get_data()
        data["type"] = StringUtils.get_string("ID_ATTRIBUTE")
        return data
