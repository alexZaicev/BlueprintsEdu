import abc
from abc import abstractmethod
from pygame.locals import *

class SceneBuilder(abc.ABC):

    def __init__(self, display, theme):
        abc.ABC.__init__(self)
        self.display = display
        self.theme = theme

    @abstractmethod
    def draw_scene(self):
        pass

    @abstractmethod
    def check_events(self, event, board):
        if event.type == QUIT:
            board.close()
