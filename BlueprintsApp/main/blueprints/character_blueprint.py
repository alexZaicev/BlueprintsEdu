from blueprints.blueprint import Blueprint


class CharacterBlueprint(Blueprint):

    def __init__(self, name=None, attributes=list(), functions=list(), sprites=()):
        Blueprint.__init__(self, type=Blueprint.TYPES.get("CHARACTER"), name=name)
        self.attributes = attributes  # DATA RELATED TO CHARACTER
        self.functions = functions
        self.sprites = sprites


