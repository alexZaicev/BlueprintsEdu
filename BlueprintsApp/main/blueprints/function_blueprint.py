from blueprints.blueprint import Blueprint


class FunctionBlueprint(Blueprint):

    def __init__(self, name=None, code=None, func_type="FUNC_C"):
        Blueprint.__init__(self, Blueprint.TYPES.get("FUNCTION"), name)
        if code is None:
            code = dict()
        self.code = code
        self.func_type = func_type

    def to_dict(self):
        r = super().to_dict()
        r["CODE"] = self.code
        r["FUNCTION_TYPE"] = self.func_type
        return r


