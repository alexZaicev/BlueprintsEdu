from blueprints.blueprint import Blueprint


class FunctionBlueprint(Blueprint):

    def __init__(self, name=None, code=None):
        Blueprint.__init__(self, Blueprint.TYPES.get("FUNCTION"), name)
        if code is None:
            code = dict()
        self.code = code


