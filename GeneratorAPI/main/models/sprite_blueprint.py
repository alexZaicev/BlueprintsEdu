from models.blueprint import Blueprint


class SpriteBlueprint(Blueprint):

    def __init__(self, data):
        Blueprint.__init__(self, data)
        self.attributes = data.get("ATTRIBUTES")
        self.functions = data.get("FUNCTIONS")

