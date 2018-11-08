from blueprints.blueprint import Blueprint


class SpriteBlueprint(Blueprint):

    def __init__(self, name=None, image=None, attributes=list(), functions=list()):
        Blueprint.__init__(self, Blueprint.TYPES.get("SPRITE"), name)
        self.image = image
        self.attributes = attributes
        self.functions = functions

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
