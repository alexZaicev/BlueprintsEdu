from utils.enums.status import Status


class Entity(object):

    def __init__(self, status=Status.NONE, project=Status.NONE, api=Status.NONE):
        object.__init__(self)
        self.status = status
        self.project = project
        self.api = api

    def to_dict(self):
        r = dict()
        r["STATUS"] = self.status
        r["PROJECT"] = self.project
        r["API"] = self.api
        return r
