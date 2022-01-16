from sqlite3 import connect

import pygame

import menu
from main import fps, terminate, load_image


class Finish:
    def __init__(self, screen, clock, winner, name_w, name_b):
        self.screen = screen
        self.size = self.width, self.height = screen.get_width(), screen.get_height()
        self.clock = clock
        self.winner = winner

        pygame.display.set_caption("Конец")
        self.fon = pygame.transform.scale(load_image('finish_fon.png'), (self.width, self.height))

        self.all_sprites = pygame.sprite.Group()
        self.buttons = pygame.sprite.Group()

        self.db_update(name_w, name_b)
        self.main()

    def db_update(self, name_w, name_b):
        con = connect('../score_table.db')
        cur = con.cursor()

        res = list(map(lambda x: x[0], cur.execute("""SELECT name FROM Rating""").fetchall()))
        for name in (name_w, name_b):
            if name_w not in res:
                query = """INSERT INTO Rating (name, all_games, white_win, black_win, winrate) 
                VALUES (?, ?, ?, ?, ?)"""
                cur.execute(query, (name, 0, 0, 0, 0)).fetchall()

        if self.winner == name_w:
            query = """UPDATE rating SET white_win = white_win + 1 WHERE name = ?"""
        elif self.winner == name_b:
            query = """UPDATE rating SET black_win = black_win + 1 WHERE name = ?"""
        if self.winner != 'Ничья':
            cur.execute(query, (self.winner,))

        for name in (name_w, name_b):
            query = """SELECT all_games, white_win, black_win FROM Rating WHERE name = ?"""
            games, white, black = cur.execute(query, (name,)).fetchall()[0]

            query = """UPDATE rating SET all_games = ?, winrate = ? WHERE name = ?"""
            cur.execute(query, (games + 1, round((white + black) / (games + 1) * 100, 2),
                                name)).fetchall()

        con.commit()

    def write(self):
        if self.winner == 'Ничья':
            text = self.winner
        else:
            text = f"Победил {self.winner}"
        intro_text = [text, 'Нажмите любую кнопку']
        font = pygame.font.Font(None, 30)
        text_coord = self.height // 2 - 40
        for line in intro_text:
            string_rendered = font.render(line, True, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = self.width // 2 - 100
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
        start_window = menu.Menu(self.screen, self.clock)
