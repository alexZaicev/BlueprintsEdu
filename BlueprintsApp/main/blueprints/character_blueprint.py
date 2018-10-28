from blueprints.blueprint import Blueprint


class CharacterBlueprint(Blueprint):

    def __init__(self):
        Blueprint.__init__(self, Blueprint.TYPES.get("CHARACTER"))
