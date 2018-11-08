from blueprints.blueprint import Blueprint


class CharacterBlueprint(Blueprint):

    def __init__(self, name=None, attributes=None, functions=None, sprites=None):
        Blueprint.__init__(self, type=Blueprint.TYPES.get("CHARACTER"), name=name)
        if functions is None:
            functions = list()
        if attributes is None:
            attributes = list()
        if sprites is None:
            sprites = list()
        self.attributes = attributes  # DATA RELATED TO CHARACTER
        self.functions = functions
        self.sprites = sprites

    def add_attribute(self, attribute):
        if attribute not in self.attributes:
            self.attributes.append(attribute)

    def add_function(self, func):
        if func not in self.functions:
            self.functions.append(func)

    def add_sprite(self, sprite):
        self.sprites.clear()
        self.sprites.append(sprite)
        # TODO implement multiple sprite object
        # if sprite not in self.sprites:
        #     self.sprites.append(sprite)
