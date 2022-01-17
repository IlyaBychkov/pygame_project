import os
import sys

import pygame

import start

fps = 60


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):  # загрузка изображения в pygame
    fullname = os.path.join('../img', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    return image


class Button(pygame.sprite.Sprite):  # класс кнопки
    def __init__(self, text, x, y, *groups):
        super().__init__(*groups)
        self.text = text
        self.font = pygame.font.Font(None, 42)
        self.text_r = self.font.render(self.text, True, pygame.Color('black'))
        self.rect = pygame.rect.Rect(*[x, y, self.text_r.get_width() + 10, self.text_r.get_height() + 6])

    def render(self, screen):
        pygame.draw.rect(screen, pygame.Color('darkgrey'), self.rect)
        screen.blit(self.text_r, (self.rect.x + 5, self.rect.y + 3))

    def check_click(self, coords):
        return self.rect.x <= coords[0] <= self.rect.x + self.rect.w and \
               self.rect.y <= coords[1] <= self.rect.y + self.rect.h

    def swap_window(self):
        return self.text

    def get_click(self, mouse_pos):
        if self.check_click(mouse_pos):
            return self.swap_window()
        return None


if __name__ == '__main__':
    pygame.init()
    clock = pygame.time.Clock()
    image = load_image('start_fon.png')
    size = width, height = image.get_width() // 2, image.get_height() // 2
    screen = pygame.display.set_mode(size)
    chess = start.Chess(screen, clock)
