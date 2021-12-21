import pygame

from main import load_image
import menu


class Chess:
    def __init__(self):
        image = load_image('fon.png')
        self.size = self.width, self.height = image.get_width() / 2, image.get_height() / 2
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Добро пожаловать в игру")
        self.fon = pygame.transform.scale(load_image('fon.png'), (self.width, self.height))
        self.fps = 60
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
                    self.start()
            pygame.display.flip()
            self.clock.tick(self.fps)

    def start(self):
        self.screen = menu.Menu()
