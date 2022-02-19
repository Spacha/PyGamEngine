#!/usr/bin/env python3
"""
This module is a sample game that is developed along with the engine.
"""
from Tanks import Tanks

def main():
    """ Main entry point of the app """

    SCR_SIZE = (800, 600)
    MAX_FPS  = 100

    tanks_game = Tanks(scr_size = SCR_SIZE, max_fps = MAX_FPS)
    tanks_game.init()
    tanks_game.run()


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
