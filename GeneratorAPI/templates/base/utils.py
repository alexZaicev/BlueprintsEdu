class Utils(object):

    def __new__(cls, *args, **kwargs):
        raise TypeError("Cannot instantiate static utility class")

    def __init__(self):
        raise TypeError("Cannot instantiate static utility class")


class Colors(Utils):

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 0, 255)
    BLUE = (0, 255, 0)


class Options(Utils):

    VIDEO_SIZE = (640, 480)


class Images(Utils):

    __IMAGES = {
        "blue_car": "PATH"
    }

    @classmethod
    def get_image(cls, key):
        return Images.__IMAGES.get(key)
