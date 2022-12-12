# python_snake_game_view.py
# author: Robin Jiang

# this module contains the gui or "view" of the snake game

import pygame

TARGET_FRAMERATE = 30

class SnakeGame:
    def __init__(self) -> None:
        self._running = True

    def run(self) -> None:
        pygame.init()
        self._resize_surface((400, 400), )
        clock = pygame.time.Clock()

        while self._running:
            clock.tick(TARGET_FRAMERATE)
            self._handle_events()
        pygame.quit()

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False

    def _resize_surface(self, size: tuple[int, int]) -> None:
        """Resizes the pygame window to the size."""
        pygame.display.set_mode(size, pygame.RESIZABLE)

if __name__ == "__main__":
    SnakeGame().run()
