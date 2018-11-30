from blueprints.blueprint import Blueprint


class CharacterBlueprint(Blueprint):

    def __init__(self, name=None, pos=None, size=None, alive=True, attributes=None, functions=None, sprites=None, color=None):
        Blueprint.__init__(self, type=Blueprint.TYPES.get("CHARACTER"), name=name)
        if pos is None:
            pos = (0, 0)
        if size is None:
            size = (0, 0)
        if functions is None:
            functions = list()
        if attributes is None:
            attributes = list()
        if sprites is None:
            sprites = list()
        self.pos = pos
        self.size = size
        self.alive = alive
        self.attributes = attributes  # DATA RELATED TO CHARACTER
        self.functions = functions
        self.sprites = sprites
        self.color = color

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

    def remove_connection(self, bp):
        if bp.get_type() == Blueprint.TYPES.get("ATTRIBUTE"):
            self.attributes.remove(bp)
        elif bp.get_type() == Blueprint.TYPES.get("FUNCTION"):
            self.functions.remove(bp)
        elif bp.get_type() == Blueprint.TYPES.get("SPRITE"):
            self.sprites.remove(bp)

    def clear_connections(self):
        self.attributes.clear()
        self.functions.clear()
        self.sprites.clear()

    def to_dict(self):
        r = super().to_dict()
        r["POSITION"] = self.pos
        r["SIZE"] = self.size
        r["ALIVE"] = self.alive
        d = list()
        for att in self.attributes:
            d.append(att.to_dict())
        r["ATTRIBUTES"] = d
        d = list()
        for func in self.functions:
            d.append(func.to_dict())
        r["FUNCTIONS"] = d
        d = list()
        for sp in self.sprites:
            d.append(sp.to_dict())
        r["SPRITES"] = d
        return r
