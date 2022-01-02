import pygame

import menu
from main import load_image, fps, terminate, Button


class Rating:
    def __init__(self, screen, clock):
        self.screen = screen
        self.size = self.width, self.height = screen.get_width(), screen.get_height()
        self.clock = clock

        pygame.display.set_caption("Рейтинг")
        self.fon = pygame.transform.scale(load_image('rating_fon.png'), (self.width, self.height))

        self.all_sprites = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()
        Button('Назад', 20, 20, self.all_sprites, self.buttons)

        self.main()

    def main(self):
        next = None
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for btn in self.buttons:
                        new = btn.get_click(event.pos)
                        if new:
                            next = new
                            running = False
            self.screen.blit(self.fon, (0, 0))
            for btn in self.buttons:
                btn.render(self.screen)
            pygame.display.flip()
            self.clock.tick(fps)
        if next == 'Назад':
            self.back()
        else:
            terminate()

    def back(self):
        menu_window = menu.Menu(self.screen, self.clock)
