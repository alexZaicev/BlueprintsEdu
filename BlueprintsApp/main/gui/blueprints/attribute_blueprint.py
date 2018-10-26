from gui.blueprints.blueprint import Blueprint


class AttributeBlueprint(Blueprint):

    def __init__(self, panel, blueprint):
        Blueprint.__init__(self, panel, "Attribute_1", blueprint)
        # TODO improve random blueprint name generation
