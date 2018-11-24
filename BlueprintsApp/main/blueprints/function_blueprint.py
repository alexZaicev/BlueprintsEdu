from blueprints.blueprint import Blueprint


class FunctionBlueprint(Blueprint):

    def __init__(self, name=None, code=None, func_type="FUNC_C",
                 orientation="ORIENT_UP", directional=False, key_press="KEY_SINGLE"):
        Blueprint.__init__(self, Blueprint.TYPES.get("FUNCTION"), name)
        if code is None:
            code = dict()
        self.code = code
        self.func_type = func_type
        self.orientation = orientation
        self.directional = directional
        self.key_press = key_press

    def to_dict(self):
        r = super().to_dict()
        r["CODE"] = self.code
        r["FUNCTION_TYPE"] = self.func_type
        r["ORIENTATION"] = self.orientation
        r["DIRECTIONAL"] = self.directional
        r["KEY_PRESS"] = self.key_press
        return r


