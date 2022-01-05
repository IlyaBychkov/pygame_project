import pygame

import game
import rating
import start
from main import load_image, fps, terminate, Button


class InputName(pygame.sprite.Sprite):
    def __init__(self, text, x, y, *groups):
        super().__init__(*groups)
        self.colors = [(0, 255, 0), (255, 0, 0)]
        self.active = False
        self.text = text
        self.num = text[-1]
        self.name_font = pygame.font.Font(None, 42)
        self.manual_font = pygame.font.Font(None, 32)
        self.rect = pygame.rect.Rect(*[x, y, 0, 0])

    def render(self, screen):
        text_r = self.name_font.render(self.text, True, pygame.Color('black'))
        self.rect.w = text_r.get_width() + 10
        self.rect.h = text_r.get_height() + 6
        pygame.draw.rect(screen, self.colors[self.active], self.rect, 2)
        screen.blit(text_r, (self.rect.x + 5, self.rect.y + 3))

        manual_r = self.manual_font.render(f'Введите ник Игрока{self.num}:', True, pygame.Color('black'))
        screen.blit(manual_r, (self.rect.x - manual_r.get_width() - 15, self.rect.y + 8))

    def check_click(self, coords):
        return self.rect.x <= coords[0] <= self.rect.x + self.rect.w and \
               self.rect.y <= coords[1] <= self.rect.y + self.rect.h

    def get_click(self, mouse_pos):
        return self.check_click(mouse_pos)


class Menu:
    def __init__(self, screen, clock):
        self.screen = screen
        self.size = self.width, self.height = screen.get_width(), screen.get_height()
        self.clock = clock

        pygame.display.set_caption("Меню")
        self.fon = pygame.transform.scale(load_image('menu_fon.png'), (self.width, self.height))

        self.all_sprites = pygame.sprite.Group()

        self.buttons = pygame.sprite.Group()
        Button('Назад', 20, 20, self.all_sprites, self.buttons)
        Button('Играть', self.width - 20 - 100, 20, self.all_sprites, self.buttons)
        Button('Рейтинг', 20, 100, self.all_sprites, self.buttons)

        self.names = pygame.sprite.Group()
        InputName('Player1', 550, 225, self.all_sprites, self.names)
        InputName('Player2', 550, 300, self.all_sprites, self.names)

        self.main()

    def main(self):
        next_window = None
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for obj in self.buttons:
                        new = obj.get_click(event.pos)
                        if new:
                            next_window = new
                            running = False
                    for obj in self.names:
                        if obj.get_click(event.pos):
                            obj.active = not obj.active
                        else:
                            obj.active = False
                elif event.type == pygame.KEYDOWN:
                    for obj in self.names:
                        if obj.active:
                            if event.key == pygame.K_BACKSPACE:
                                obj.text = obj.text[:-1]
                            elif event.key in (pygame.K_RETURN, pygame.K_ESCAPE, pygame.K_TAB):
                                obj.active = False
                            else:
                                if len(obj.text) < 15:
                                    obj.text += event.unicode
            self.screen.blit(self.fon, (0, 0))
            for obj in self.all_sprites:
                obj.render(self.screen)
            pygame.display.flip()
            self.clock.tick(fps)
        if next_window == 'Назад':
            self.back()
        elif next_window == 'Играть':
            self.start_game()
        elif next_window == 'Рейтинг':
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
