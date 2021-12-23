import pygame

import start
from main import fps, terminate, load_image


class Finish:
    def __init__(self, screen, clock, winner):
        self.screen = screen
        self.size = self.width, self.height = screen.get_width(), screen.get_height()
        self.clock = clock
        self.winner = winner

        pygame.display.set_caption("Конец")
        self.fon = pygame.transform.scale(load_image('finish_fon.png'), (self.width, self.height))

        self.all_sprites = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()

        self.main()

    def write(self):
        intro_text = [f"Победили {self.winner}", 'Нажмите любую кнопку']
        font = pygame.font.Font(None, 30)
        text_coord = self.height // 2 - 15
        for line in intro_text:
            string_rendered = font.render(line, True, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = self.width // 2 - 50
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
        self.back()

    def back(self):
        start_window = start.Chess(self.screen, self.clock)
