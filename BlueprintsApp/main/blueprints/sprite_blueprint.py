from blueprints.blueprint import Blueprint


class SpriteBlueprint(Blueprint):

    def __init__(self, name=None, image=None, attributes=list(), functions=list()):
        Blueprint.__init__(self, Blueprint.TYPES.get("SPRITE"), name)
        self.image = image
        self.attributes = attributes
        self.functions = functions
