from models.blueprint import Blueprint


class AttributeBlueprint(Blueprint):

    def __init__(self, data=None):
        Blueprint.__init__(self, data)
        self.__data_type, self.__value = data.get("DATA")

    def blueprint_data(self):
        super().blueprint_data()

    def to_dict(self):
        r = super().to_dict()
        r["data"] = {
            "type": self.__data_type,
            "value": self.__value
        }

