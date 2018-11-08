from abc import ABC, abstractmethod


class Blueprint(ABC):

    def __init__(self, data):
        if data is not None:
            self.__x, self.__y = data.get("COORDS")
            self.__width, self.__height = data.get("SIZE")
            self.__name, self.__type = data.get("NAME"), data.get("TYPE")
        else:
            raise AttributeError("Blueprint data cannot be None")

    def rect_data(self):
        return (self.__x, self.__y), (self.__width, self.__height)

    @abstractmethod
    def blueprint_data(self):
        return self.__name, self.__type

    @abstractmethod
    def to_dict(self):
        return {
            "x": self.__x,
            "y": self.__y,
            "width": self.__width,
            "height": self.__height,
            "name": self.__name,
            "type": self.__type
        }