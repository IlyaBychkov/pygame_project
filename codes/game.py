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
            self.clock.tick(fps)

    def render(self):
        pygame.draw.rect(self.screen, 'white',
                         [self.board.left - self.board.width_frame,
                          self.board.top - self.board.width_frame,
                          self.board.cell_size * self.board.width + self.board.width_frame * 2,
                          self.board.cell_size * self.board.height + self.board.width_frame * 2])
        colors = [(255, 165, 0), (165, 42, 42)]
        for i in range(self.board.width):
            for j in range(self.board.height):
                r, g, b = colors[(i + j) % 2]
                if i == self.x and j == self.y:
                    r = b = 0
                pygame.draw.rect(self.screen, (r, g, b),
                                 [self.board.left + self.board.cell_size * i,
                                  self.board.top + self.board.cell_size * j,
                                  self.board.cell_size, self.board.cell_size])
        self.all_sprites = pygame.sprite.Group()
        for i in range(self.board.width):
            for j in range(self.board.height):
                if self.board.cell(i, j) != '  ':
                    figure = pygame.sprite.Sprite(self.all_sprites)
                    img = self.images[self.board.cell(i, j)]
                    koeff = (self.board.cell_size - 5) / img.get_height()
                    figure.image = pygame.transform.scale(self.images[self.board.cell(i, j)], (
                        img.get_width() * koeff, img.get_height() * koeff))
                    figure.rect = figure.image.get_rect()
                    figure.rect.center = self.board.left + int(self.board.cell_size * (j + 0.5)), \
                                         self.board.left + int(self.board.cell_size * (7 - i + 0.5))

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.board.left) // self.board.cell_size
        cell_y = (mouse_pos[1] - self.board.top) // self.board.cell_size
        if cell_x < 0 or cell_x >= self.board.width or cell_y < 0 or cell_y >= self.board.height:
            return None
        return cell_x, 7 - cell_y

    def on_click(self, cell):
        if self.board.cell(cell[1], cell[0]) != '  ':
            self.x, self.y = cell[0], 7 - cell[1]
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
