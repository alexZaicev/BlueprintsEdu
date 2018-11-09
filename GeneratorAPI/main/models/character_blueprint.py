from models.blueprint import Blueprint


class CharacterBlueprint(Blueprint):

    def __init__(self, data):
        Blueprint.__init__(self, data)
        self.attributes = data.get("ATTRIBUTES")
        self.functions = data.get("FUNCTIONS")
        self.sprites = data.get("SPRITES")

