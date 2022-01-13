import sqlite3

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

        con = sqlite3.connect('../score_table.db')
        self.cur = con.cursor()
        self.font = pygame.font.Font(None, 40)
        self.main()

    def print_text(self, text, x, y):
        render = self.font.render(text, True, (255, 255, 255))
        self.rect = pygame.Rect(x, y, render.get_width(), render.get_height())
        self.screen.blit(render, self.rect)

    def print_board(self):
        x, y = 80, 100
        step_x, step_y = 200, 70
        res = list(self.cur.execute("""select * from rating order by -winrate""").fetchall())
        res = [('№', 'Name', 'Games', 'White', 'Black', '% win')] + res[:min(len(res), 5)]
        id = 0
        for querry in res:
            self.print_text(str(id), x, y)
            x += step_x // 2
            for text in range(1, len(querry)):
                self.print_text(str(querry[text]), x, y)
                x += step_x // 2
                if text == 1:
                    x += step_x
            x -= step_x * (len(querry) - 2)
            y += step_y
            id += 1

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
            self.print_board()
            pygame.display.flip()
            self.clock.tick(fps)
        if next == 'Назад':
            self.back()
        else:
            terminate()

    def back(self):
        menu_window = menu.Menu(self.screen, self.clock)
