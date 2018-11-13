import pygame as pg


class Sprite(object):

    def __init__(self, pos, size, image, alive=True):
        self.pos = pos
        self.size = size
        self.image = pg.transform.scale(pg.image.load(image), self.size)
        self.alive = alive

    def get_rect(self):
        rect = self.image.get_rect()
        rect.topleft = self.pos
        return rect

    def draw(self, display):
        pass

    def events_handler(self, event):
        pass
