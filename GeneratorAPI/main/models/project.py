from models.entity import Entity
from models.attribute_blueprint import AttributeBlueprint
from models.sprite_blueprint import SpriteBlueprint
from models.function_blueprint import FunctionBlueprint
from models.character_blueprint import CharacterBlueprint


class ProjectModel(Entity):

    def __init__(self, name="Undefined_Project", api="undefined", characters=None, attributes=None, functions=None, sprites=None):
        Entity.__init__(self, project=name, api=api)
        self.name = name
        self.api = api
        self.attributes = list()
        self.functions = list()
        self.characters = list()
        self.sprites = list()
        self.__init_project_data(characters, attributes, functions, sprites)

    def __init_project_data(self, characters, attributes, functions, sprites):
        if characters is not None:
            for b in characters:
                self.add_character(b)
        if attributes is not None:
            for b in attributes:
                self.add_attribute(b)
        if functions is not None:
            for b in functions:
                self.add_function(b)
        if sprites is not None:
            for b in sprites:
                self.add_sprite(b)

    def add_attribute(self, ab):
        if isinstance(ab, AttributeBlueprint):
            for b in self.attributes:
                if b.name == ab.name:
                    break
            else:
                self.attributes.append(ab)
        else:
            raise AttributeError("Invalid attribute blueprint type provided: {}".format(str(type(ab))[8:-2]))

    def add_function(self, fb):
        if isinstance(fb, FunctionBlueprint):
            for b in self.functions:
                if b.name == fb.name:
                    break
            else:
                self.functions.append(fb)
        else:
            raise AttributeError("Invalid function blueprint type provided: {}".format(str(type(fb))[8:-2]))

    def add_sprite(self, sb):
        if isinstance(sb, SpriteBlueprint):
            for b in self.sprites:
                if b.name == sb.name:
                    break
            else:
                self.sprites.append(sb)
        else:
            raise AttributeError("Invalid sprite blueprint type provided: {}".format(str(type(sb))[8:-2]))

    def add_character(self, cb):
        if isinstance(cb, CharacterBlueprint):
            for b in self.characters:
                if b.name == cb.name:
                    break
            else:
                self.characters.append(cb)
        else:
            raise AttributeError("Invalid character blueprint type provided: {}".format(str(type(cb))[8:-2]))

    def to_dict(self):
        d = super().to_dict()
        a, f, s = list(), list(), list()
        for b in self.attributes:
            a.append(b.to_dict())
        for b in self.functions:
            f.append(b.to_dict())
        for b in self.sprites:
            s.append(b.to_dict())
        d["ATTRIBUTES"] = a
        d["FUNCTIONS"] = f
        d["SPRITES"] = s
        return d

