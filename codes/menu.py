import pygame

import game
import rating
import start
from main import load_image, fps, terminate, Button


class Menu:
    def __init__(self, screen, clock):
        self.screen = screen
        self.size = self.width, self.height = screen.get_width(), screen.get_height()
        self.clock = clock

        pygame.display.set_caption("Меню")
        self.fon = pygame.transform.scale(load_image('menu_fon.png'), (self.width, self.height))

        self.all_sprites = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()
        Button('Назад', 20, 20, 100, 30, self, self.all_sprites, self.buttons)
        Button('Играть', self.width - 20 - 100, 20, 100, 30, self, self.all_sprites, self.buttons)
        Button('Рейтинг', 20, 100, 150, 30, self, self.all_sprites, self.buttons)

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
        elif next == 'Играть':
            self.start_game()
        elif next == 'Рейтинг':
            self.rating()
        else:
            terminate()

    def start_game(self):
        game_window = game.Game(self.screen, self.clock)

    def change_game(self):
        pass

    def change_names(self):
        pass

    def rating(self):
        rating_window = rating.Rating(self.screen, self.clock)

    def back(self):
        start_window = start.Chess(self.screen, self.clock)
