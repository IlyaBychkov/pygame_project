import os
import sys

import pygame

import start

fps = 60


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
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
    else:
        pass
        # image = image.convert_alpha()
    return image


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
