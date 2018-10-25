from utils import logger_utils
from board import Board
import pygame, os
import config_loader

os.path.join(os.path.split(__file__)[0], "resources")
os.environ['SDL_VIDEO_CENTERED'] = '1'

def main():
    logger = logger_utils.get_logger(__name__)
    logger.info("Application started")
    board = Board()
    session = board.run()

if __name__ == "__main__":
    __name__ = "main"
    main()
