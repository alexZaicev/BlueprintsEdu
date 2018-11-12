"""Description: BLueprints module contains blueprint base class with sharing attributes and methodsself.
To clarify we will refer to character/sprite blueprint as game object, function as game object behaviour
and attribute as special game object data.

In the app there can be various types of blueprints:
    >> FUNCTION : is a method that user can edit/create from scratch in the development process. It contains
            some special logic for any game object
    >> CHARACTER : is the main game object that the user controls by using blurptints. User is allowed to add
            attributes/functions to the game object to variously manipulate itself
    >> SPRITE : is an image that can represent any game object. User is allowed to add behaviour to that object
            by using the same principle as with the character
    >> ATTRIBUTE : is a special game object data type that may contain any data inside and it can be used by
            the user to create behaviour
"""
from abc import ABC, abstractmethod
from utils.string_utils import StringUtils


class Blueprint(ABC):

    TYPES = {
        "FUNCTION": "BT_0",
        "CHARACTER": "BT_1",
        "SPRITE": "BT_2",  # IMAGE
        "ATTRIBUTE": "BT_3"
    }

    NAME_COUNT = 1

    def __init__(self, type, name):
        self.__type = type
        if name is None:
            self.name = "{}_{}".format(StringUtils.get_string("ID_UNKNOWN"), Blueprint.NAME_COUNT)
            Blueprint.NAME_COUNT += 1
        else:
            self.name = name

    def get_type(self):
        return self.__type

    @abstractmethod
    def to_dict(self):
        return {
            "NAME": self.name,
            "TYPE": self.__type
        }
