from blueprints.blueprint import Blueprint


class SpriteBlueprint(Blueprint):

    def __init__(self):
        Blueprint.__init__(self, Blueprint.TYPES.get("SPRITE"))
