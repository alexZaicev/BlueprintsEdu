from utils.enums.status import Status


class Entity(object):

    def __init__(self, status=Status.NONE, data=None):
        object.__init__(self)
        self.status = status
        if data is None:
            self.data = dict()
        else:
            self.data = data

    def to_dict(self):
        r = dict()
        r["STATUS"] = self.status
        r["DATA"] = self.data
        return r
