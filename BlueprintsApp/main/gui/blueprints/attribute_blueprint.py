from gui.blueprints.blueprint import Blueprint
from utils.string_utils import StringUtils
from blueprints.attribute_blueprint import AttributeBlueprint as AB


class AttributeBlueprint(Blueprint):

    SIZE = [.2, .1]

    def __init__(self, panel):
        Blueprint.__init__(self, panel, "{}_1".format(StringUtils.get_string("ID_ATTRIBUTE")), AB())
        # TODO improve random blueprint name generation
        self.set_custom_size(AttributeBlueprint.SIZE)

    def get_data(self):
        data = super().get_data()
        data["type"] = StringUtils.get_string("ID_ATTRIBUTE")
        return data
