import pygame

import chesses
from main import fps, load_image


class Game:
    def __init__(self, screen, size):
        self.board = chesses.Board(8, 8, 100, 100, 50, 3)
        self.board.width_frame = 3
        self.screen = screen
        self.size = self.width, self.height = size
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
        pygame.display.set_caption("Добро пожаловать в игру")
        self.all_sprites = pygame.sprite.Group()
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
        self.clock = pygame.time.Clock()
        self.main()

    def main(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.get_click(event.pos)
            self.screen.fill((0, 0, 0))
            self.render()
            self.all_sprites.draw(self.screen)
            pygame.display.flip()
            # self.clock.tick(fps)

    def render(self):
        pygame.draw.rect(self.screen, 'white',
                         [self.board.left - self.board.width_frame,
                          self.board.top - self.board.width_frame,
                          self.board.cell_size * self.board.width + self.board.width_frame * 2,
                          self.board.cell_size * self.board.height + self.board.width_frame * 2])
        colors = [(240, 218, 181), (181, 131, 99), (242, 130, 116), (212, 89, 74), (245, 236, 115), (216, 194, 74)]
        for i in range(self.board.width):
            for j in range(self.board.height):
                x = 7 - i
                y = j
                r, g, b = colors[(i + j) % 2]
                if (x == self.x and y == self.y) or self.board.field[self.x][self.y].can_move(
                        self.board, self.x, self.y, x, y) and not self.board.field[x][y]:
                    if (i + j) % 2:
                        r, g, b = colors[5]
                    else:
                        r, g, b = colors[4]
                elif (x != self.x or y != self.y) and self.board.field[self.x][self.y].can_attack(
                        self.board, self.x, self.y, x, y) and self.board.field[x][y] and \
                        self.board.field[x][y].color != self.board.field[self.x][self.y].color:
                    if (i + j) % 2:
                        r, g, b = colors[3]
                    else:
                        r, g, b = colors[2]
                pygame.draw.rect(self.screen, (r, g, b),
                                 [self.board.left + self.board.cell_size * j,
                                  self.board.top + self.board.cell_size * i,
                                  self.board.cell_size, self.board.cell_size])

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.board.left) // self.board.cell_size
        cell_y = (mouse_pos[1] - self.board.top) // self.board.cell_size
        if cell_x < 0 or cell_x >= self.board.width or cell_y < 0 or cell_y >= self.board.height:
            return None
        return cell_x, 7 - cell_y

    def get_coords(self, x, y):
        return (self.board.left + int(self.board.cell_size * (y + 0.5)), self.board.left + int(
            self.board.cell_size * (7 - x + 0.5)))

    def on_click(self, cell):
        y, x = cell
        if self.x != -1:
            # print(self.get_coords(x, y))
            self.board.field[self.x][self.y].sprite.rect.center = self.get_coords(x, y)
            pygame.sprite.spritecollide(self.board.field[self.x][self.y].sprite, self.all_sprites, True)
            self.all_sprites.add(self.board.field[self.x][self.y].sprite)
            self.board.field[x][y] = self.board.field[self.x][self.y]
            self.board.field[self.x][self.y] = None
            self.x = self.y = -1
        elif self.board.cell(cell[1], cell[0]) != '  ':
            self.y, self.x = cell
        else:
            self.x = self.y = -1

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)

    def opponent(self):
        pass

    def check_mat(self):
        pass

    def finish(self):
        pass
