from blueprints.blueprint import Blueprint


class SpriteBlueprint(Blueprint):

    def __init__(self, name=None, image=None, attributes=None, functions=None):
        Blueprint.__init__(self, Blueprint.TYPES.get("SPRITE"), name)
        self.image = image
        if attributes is None:
            self.attributes = list()
        if functions is None:
            self.functions = list()

    def add_attribute(self, attribute):
        if attribute not in self.attributes:
            self.attributes.append(attribute)

    def add_function(self, func):
        if func not in self.functions:
            self.functions.append(func)

    def remove_connection(self, bp):
        if bp.get_type() == Blueprint.TYPES.get("ATTRIBUTE"):
            self.attributes.remove(bp)
        elif bp.get_type() == Blueprint.TYPES.get("FUNCTION"):
            self.functions.remove(bp)

    def clear_connections(self):
        self.attributes.clear()
        self.functions.clear()

    def to_dict(self):
        r = super().to_dict()
        d = list()
        for att in self.attributes:
            d.append(att.to_dict())
        r["ATTRIBUTES"] = d
        d.clear()
        for func in self.functions:
            d.append(func.to_dict())
        r["FUNCTIONS"] = d
        return r