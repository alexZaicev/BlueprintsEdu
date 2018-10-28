from blueprints.blueprint import Blueprint


class AttributeBlueprint(Blueprint):

    def __init__(self):
        Blueprint.__init__(self, Blueprint.TYPES.get("ATTRIBUTE"))
