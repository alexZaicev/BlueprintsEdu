"""Description: Blueprints Manager is a special module that`s parses blueprint connections into
project '.blue' file configuration and loads that configuration to generate a working copy of a
selected game API
"""


class BlueprintManager(object):

    def __init__(self):
        object.__init__(self)
        raise TypeError("Cannot instantiate static managers")

    @classmethod
    def parse_blueprints(cls, bp_conns):
        """Description: Function analyses and creates XML-format .bp files from
        blueprint connections.
        """
        return cfg = ""

    def reverse_parse_blueprints(cls, contents):
        """Descripion: Function parses XML-format .bp file contents into relevent
        blueprint object
        """
        return list(list())

    def __parse_attribute(self, data):
        pass

    def __parse_function(self, data):
        pass

    def __parse_sprite(self, data):
        pass

    def __parse_character(self, data):
        pass

    def __reverse_parse_attribute(self, data):
        pass

    def __reverse_parse_function(self, data):
        pass

    def __reverse_parse_sprite(self, data):
        pass

    def __reverse_parse_character(self, data):
        pass
