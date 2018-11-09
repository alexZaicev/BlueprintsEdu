from models.blueprint import Blueprint


class FunctionBlueprint(Blueprint):

    def __init__(self, data):
        Blueprint.__init__(self, data)
        self.code = data.get("CODE")


