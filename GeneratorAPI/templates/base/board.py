import pygame as pg
from pygame.locals import *
from utils import *


class Board(object):

    def __init__(self):
        pg.init()
        pg.display.set_caption(" --- Car Simulator --- ")
        self.fps = 90
        self.running = True
        self.clock = pg.time.Clock()
        self.display = pg.display.set_mode(Options.VIDEO_SIZE)
        self.characters = self.init_characters()
        self.sprites = self.init_sprites()

    def init_characters(self):
        # GENERATOR TAGS REQUIRED
        return list()

    def init_sprites(self):
        # GENERATOR TAGS REQUIRED
        return list()

    def start(self):
        while self.running:
            for event in pg.event.get():
                self.events_handler(event)

            self.draw()

            pg.display.flip()
            self.clock.tick(self.fps)
        pg.quit()

    def draw(self):
        self.display.fill(Colors.WHITE)
        for char in self.characters:
            char.draw(self.display)
        for sp in self.sprites:
            sp.draw(self.display)

    def events_handler(self, event):
        if event.type == QUIT:
            self.running = False
        elif event.type == KEYDOWN or event.type == KEYUP:
            if event.key == K_ESCAPE:
                self.running = False
