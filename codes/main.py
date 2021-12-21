import os
import sys

import pygame

import start


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


if __name__ == '__main__':
    pygame.init()
    size = weight, height = 500, 500
    screen = start.Chess()
