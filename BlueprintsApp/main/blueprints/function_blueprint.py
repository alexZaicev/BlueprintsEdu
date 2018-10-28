from blueprints.blueprint import Blueprint


class FunctionBlueprint(Blueprint):

    def __init__(self):
        Blueprint.__init__(self, Blueprint.TYPES.get("FUNCTION"))
