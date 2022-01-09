import pygame

import chesses
import finish
from chesses import BLACK
from main import fps, load_image, terminate


class Game:
    def __init__(self, screen, clock):
        self.board = chesses.Board(8, 8, 100, 100, 50, 3)
        self.board.width_frame = 3
        self.screen = screen
        self.size = self.width, self.height = screen.get_width(), screen.get_height()
        self.clock = clock
        self.x = self.y = -1
        self.images = {
            'bB': load_image('kit_figures1/bishop_black.png'),
            'wB': load_image('kit_figures1/bishop_white.png'),
            'bK': load_image('kit_figures1/king_black.png'),
            'wK': load_image('kit_figures1/king_white.png'),
            'bN': load_image('kit_figures1/knight_black.png'),
            'wN': load_image('kit_figures1/knight_white.png'),
            'bP': load_image('kit_figures1/pawn_black.png'),
            'wP': load_image('kit_figures1/pawn_white.png'),
            'bQ': load_image('kit_figures1/queen_black.png'),
            'wQ': load_image('kit_figures1/queen_white.png'),
            'bR': load_image('kit_figures1/rook_black.png'),
            'wR': load_image('kit_figures1/rook_white.png')
        }
        pygame.display.set_caption("Шахматы")
        self.all_sprites = pygame.sprite.Group()
        self.chooze_white_sprites = pygame.sprite.Group()
        self.chooze_black_sprites = pygame.sprite.Group()
        self.white = []
        self.black = []
        a = ['wQ', 'wR', 'wB', 'wN']
        b = ['bQ', 'bR', 'bB', 'bN']
        for i in range(4):
            self.white.append(pygame.sprite.Sprite(self.chooze_white_sprites))
            img = self.images[a[i]]
            koeff = (self.board.cell_size - 5) / img.get_height()
            self.white[i].image = pygame.transform.scale(
                self.images[a[i]], (img.get_width() * koeff, img.get_height() * koeff))

            self.white[i].rect = self.white[i].image.get_rect()

            self.white[i].rect.center = 630 + int(self.board.cell_size * (i + 0.5)), \
                                        300 + int(self.board.cell_size * 0.5)

            self.black.append(pygame.sprite.Sprite(self.chooze_black_sprites))
            img = self.images[b[i]]
            koeff = (self.board.cell_size - 5) / img.get_height()
            self.black[i].image = pygame.transform.scale(
                self.images[b[i]], (img.get_width() * koeff, img.get_height() * koeff))

            self.black[i].rect = self.black[i].image.get_rect()

            self.black[i].rect.center = 630 + int(self.board.cell_size * (i + 0.5)), \
                                        300 + int(self.board.cell_size * 0.5)
        for i in range(self.board.width):
            for j in range(self.board.height):
                if self.board.cell(i, j) != '  ':
                    self.board.field[i][j].sprite = pygame.sprite.Sprite(self.all_sprites)
                    img = self.images[self.board.cell(i, j)]
                    koeff = (self.board.cell_size - 5) / img.get_height()
                    self.board.field[i][j].sprite.image = pygame.transform.scale(
                        self.images[self.board.cell(i, j)], (
                            img.get_width() * koeff, img.get_height() * koeff))

                    self.board.field[i][j].sprite.rect = self.board.field[i][
                        j].sprite.image.get_rect()

                    self.board.field[i][j].sprite.rect.center = self.board.left + int(
                        self.board.cell_size * (j + 0.5)), self.board.left + int(
                        self.board.cell_size * (
                                7 - i + 0.5))
        self.pawn_x = self.pawn_y = -1
        self.chooze_fig_fl = 0
        self.main()

    def main(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.get_click(event.pos)
            self.screen.fill((0, 0, 0))
            self.render()
            self.all_sprites.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(fps)
        self.finish(1)

    def render(self):
        pygame.draw.rect(self.screen, 'white',
                         [self.board.left - self.board.width_frame,
                          self.board.top - self.board.width_frame,
                          self.board.cell_size * self.board.width + self.board.width_frame * 2,
                          self.board.cell_size * self.board.height + self.board.width_frame * 2])
        colors = [(240, 218, 181), (181, 131, 99), (242, 130, 116), (212, 89, 74), (245, 236, 115),
                  (216, 194, 74)]
        for i in range(self.board.width):
            for j in range(self.board.height):
                x = 7 - i
                y = j
                r, g, b = colors[(i + j) % 2]
                if (x == self.x and y == self.y) or self.board.move_piece(self.x, self.y, x, y, 0) \
                        and not self.board.field[x][y]:
                    if (i + j) % 2:
                        r, g, b = colors[5]
                    else:
                        r, g, b = colors[4]
                elif (x != self.x or y != self.y) and self.board.move_piece(self.x, self.y, x, y, 0) \
                        and self.board.field[x][y] and \
                        self.board.field[x][y].color != self.board.field[self.x][self.y].color:
                    if (i + j) % 2:
                        r, g, b = colors[3]
                    else:
                        r, g, b = colors[2]
                pygame.draw.rect(self.screen, (r, g, b),
                                 [self.board.left + self.board.cell_size * j,
                                  self.board.top + self.board.cell_size * i,
                                  self.board.cell_size, self.board.cell_size])
        if self.chooze_fig_fl:
            self.draw_chooze_fig()
        # if self.board.current_player_color() == WHITE:
        #     print('Ход белых:')
        # else:
        #     print('Ход чёрных:')

    def draw_chooze_fig(self):
        top, left = 630, 300
        pygame.draw.rect(self.screen, (181, 131, 99),
                         [top - self.board.width_frame,
                          left - self.board.width_frame,
                          self.board.cell_size * 4 + self.board.width_frame * 2,
                          self.board.cell_size + self.board.width_frame * 2])
        pygame.draw.rect(self.screen, 'white',
                         [top, left, self.board.cell_size * 4, self.board.cell_size])
        if self.chooze_fig_fl == 2:
            self.chooze_white_sprites.draw(self.screen)
        else:
            self.chooze_black_sprites.draw(self.screen)

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.board.left) // self.board.cell_size
        cell_y = (mouse_pos[1] - self.board.top) // self.board.cell_size
        if cell_x < 0 or cell_x >= self.board.width or cell_y < 0 or cell_y >= self.board.height:
            return None
        return cell_x, 7 - cell_y

    def on_click(self, cell):
        if self.chooze_fig_fl:
            return
        y, x = cell
        if self.x != -1:
            if self.board.move_piece(self.x, self.y, x, y):
                self.board.NUM += 1
                self.board.field[x][y].sprite.rect.center = self.board.get_coords(x, y)
                pygame.sprite.spritecollide(self.board.field[x][y].sprite,
                                            self.all_sprites, True)
                fl = self.board.check_mat()
                if fl:
                    self.finish(fl)
                fin = 7 if self.board.color == BLACK else 0
                if fin == x and type(self.board.get_piece(x, y)) is chesses.Pawn:
                    clr = self.board.opponent(self.board.color)
                    self.pawn_x, self.pawn_y = x, y
                    self.chooze_fig_fl = clr + 1
                    self.board.field[x][y].sprite = pygame.sprite.Sprite(self.all_sprites)
                    img = self.images[self.board.cell(x, y)]
                    koeff = (self.board.cell_size - 5) / img.get_height()
                    self.board.field[x][y].sprite.image = pygame.transform.scale(
                        self.images[self.board.cell(x, y)], (
                            img.get_width() * koeff, img.get_height() * koeff))

                    self.board.field[x][y].sprite.rect = self.board.field[x][
                        y].sprite.image.get_rect()

                    self.board.field[x][y].sprite.rect.center = self.board.get_coords(x, y)
                else:
                    self.all_sprites.add(self.board.field[x][y].sprite)
                self.x = self.y = -1
            else:
                piece = self.board.get_piece(x, y)
                if piece is not None and piece.color == self.board.color:
                    self.x, self.y = x, y
                else:
                    self.x = self.y = -1
        elif self.board.cell(cell[1], cell[0]) != '  ':
            piece = self.board.get_piece(x, y)
            if piece is not None and piece.color == self.board.color:
                self.x, self.y = x, y
            else:
                self.x = self.y = -1
        else:
            self.x = self.y = -1
        self.board.print_board()

    def get_click(self, mouse_pos):
        if self.chooze_fig_fl:
            cell_x = (mouse_pos[0] - 630) // self.board.cell_size
            cell_y = (mouse_pos[1] - 300) // self.board.cell_size
            if cell_x < 0 or cell_x >= 4 or cell_y < 0 or cell_y >= 1:
                return None
            self.board.field[self.pawn_x][self.pawn_y].sprite.kill()
            if cell_x == 3:
                self.board.field[self.pawn_x][self.pawn_y] = chesses.Knight(self.chooze_fig_fl - 1)
            elif cell_x == 2:
                self.board.field[self.pawn_x][self.pawn_y] = chesses.Bishop(self.chooze_fig_fl - 1)
            elif cell_x == 1:
                self.board.field[self.pawn_x][self.pawn_y] = chesses.Rook(self.chooze_fig_fl - 1)
            elif cell_x == 0:
                self.board.field[self.pawn_x][self.pawn_y] = chesses.Queen(self.chooze_fig_fl - 1)
            self.board.field[self.pawn_x][self.pawn_y].sprite = pygame.sprite.Sprite(
                self.all_sprites)
            img = self.images[self.board.cell(self.pawn_x, self.pawn_y)]
            koeff = (self.board.cell_size - 5) / img.get_height()
            self.board.field[self.pawn_x][self.pawn_y].sprite.image = pygame.transform.scale(
                self.images[self.board.cell(self.pawn_x, self.pawn_y)], (
                    img.get_width() * koeff, img.get_height() * koeff))

            self.board.field[self.pawn_x][self.pawn_y].sprite.rect = self.board.field[self.pawn_x][
                self.pawn_y].sprite.image.get_rect()

            self.board.field[self.pawn_x][self.pawn_y].sprite.rect.center = self.board.get_coords(
                self.pawn_x, self.pawn_y)
            self.chooze_fig_fl = 0
            return None
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)
        return cell

    def finish(self, fl):  # 1 - мат, 2 - пат
        print(fl)
        clr = self.board.opponent(self.board.color)
        finish_window = finish.Finish(self.screen, self.clock, clr, fl)
