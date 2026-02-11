from game.game import BreakoutGame
import pygame


if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()

    while True:
        game = BreakoutGame()
        result = game.run()

        if result is not True:
            break

    pygame.quit()