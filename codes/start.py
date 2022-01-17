import pygame

from main import fps, load_image, terminate

import menu


class Chess:
    def __init__(self, screen, clock):
        self.screen = screen
        self.size = self.width, self.height = screen.get_width(), screen.get_height()
        self.clock = clock

        pygame.display.set_caption("Добро пожаловать в игру")
        self.fon = pygame.transform.scale(load_image('start_fon.png'), (self.width, self.height))

        self.main()

    def write(self):  # вывод текста
        intro_text = ["Нажмите любую кнопку, чтобы начать"]
        font = pygame.font.Font(None, 30)
        text_coord = self.height // 2 - 15
        for line in intro_text:
            string_rendered = font.render(line, True, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = self.width // 2 - 200
            text_coord += intro_rect.height
            self.screen.blit(string_rendered, intro_rect)

    def main(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                    return
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    running = False
            self.screen.blit(self.fon, (0, 0))
            self.write()
            pygame.display.flip()
            self.clock.tick(fps)
        self.start()

    def start(self):
        menu_window = menu.Menu(self.screen, self.clock)
