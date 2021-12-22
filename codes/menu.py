import pygame

import game
import start
from main import load_image, fps, terminate


class Button(pygame.sprite.Sprite):
    def __init__(self, text, x, y, width, height, menu, *groups):
        super().__init__(*groups)
        self.text = text
        self.menu_window = menu
        self.pos = [x, y, width, height]
        self.rect = pygame.rect.Rect(*self.pos)
        self.font = pygame.font.Font(None, 42)

    def render(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)
        string_rendered = self.font.render(self.text, True, pygame.Color('black'))
        screen.blit(string_rendered, self.rect)

    def check_click(self, coords):
        return self.pos[0] <= coords[0] <= self.pos[0] + self.pos[2] and \
               self.pos[1] <= coords[1] <= self.pos[1] + self.pos[3]

    def swap_window(self):
        if self.text == 'Назад':
            return 0
        elif self.text == 'Играть':
            return 1

    def get_click(self, mouse_pos):
        if self.check_click(mouse_pos):
            return self.swap_window()
        return -1


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

        self.main()

    def main(self):
        next = -1
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for btn in self.buttons:
                        new = btn.get_click(event.pos)
                        if new != -1:
                            next = new
                            running = False
            self.screen.blit(self.fon, (0, 0))
            for btn in self.buttons:
                btn.render(self.screen)
            pygame.display.flip()
            self.clock.tick(fps)
        if next == 0:
            self.back()
        elif next == 1:
            self.start_game()
        else:
            terminate()

    def start_game(self):
        game_window = game.Game(self.screen, self.clock)

    def change_game(self):
        pass

    def change_names(self):
        pass

    def rating(self):
        pass

    def back(self):
        start_window = start.Chess(self.screen, self.clock)
