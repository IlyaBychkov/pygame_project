import pygame

import game
from main import fps
from main import load_image


class Chess:
    def __init__(self, screen, size):
        self.screen = screen
        self.size = self.width, self.height = size
        pygame.display.set_caption("Добро пожаловать в игру")
        self.fon = pygame.transform.scale(load_image('fon.png'), (self.width, self.height))
        self.clock = pygame.time.Clock()
        self.screen.blit(self.fon, (0, 0))
        self.main()

    def main(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    running = False
            pygame.display.flip()
            self.clock.tick(fps)
        self.start()

    def start(self):
        wind = game.Game(self.screen, self.size)
