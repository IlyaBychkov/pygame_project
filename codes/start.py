import pygame


class Chess:
    def __init__(self):
        self.size = self.weight, self.height = 500, 500
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption("Добро пожаловать в игру")
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.screen.fill((0, 0, 0))
            pygame.display.flip()
        pygame.quit()

    def start(self):
        pass

    def exit(self):
        pass