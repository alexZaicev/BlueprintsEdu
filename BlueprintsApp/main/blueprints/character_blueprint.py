from blueprints.blueprint import Blueprint


class CharacterBlueprint(Blueprint):

    def __init__(self, name=None):
        Blueprint.__init__(self, type=Blueprint.TYPES.get("CHARACTER"), name=name)
