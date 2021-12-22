import pygame

import chesses
from main import fps, load_image


class Board:
    def __init__(self, width, height, left=10, top=10, cell_size=10, width_frame=2):
        self.width = width
        self.height = height
        self.board = [[0 for __ in range(width)] for _ in range(height)]
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.width_frame = width_frame

    def render(self, screen):
        pygame.draw.rect(screen, 'white',
                         [self.left - self.width_frame, self.top - self.width_frame,
                          self.cell_size * self.width + self.width_frame * 2,
                          self.cell_size * self.height + self.width_frame * 2])
        colors = ['orange', 'brown']
        for i in range(self.width):
            for j in range(self.height):
                pygame.draw.rect(screen, colors[(i + j) % 2],
                                 [self.left + self.cell_size * i,
                                  self.top + self.cell_size * j,
                                  self.cell_size, self.cell_size])

    def get_cell(self, mouse_pos):
        cell_x = (mouse_pos[0] - self.left) // self.cell_size
        cell_y = (mouse_pos[1] - self.top) // self.cell_size
        if cell_x < 0 or cell_x >= self.width or cell_y < 0 or cell_y >= self.height:
            return None
        return cell_x, cell_y

    def on_click(self, cell):
        print(cell)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell:
            self.on_click(cell)


class Game:
    def __init__(self, screen, size):
        self.board = Board(8, 8, 100, 100, 50, 3)
        self.screen = screen
        self.chess = chesses.Board()
        self.size = self.width, self.height = size
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
                    self.board.get_click(event.pos)
            self.screen.fill((0, 0, 0))
            self.board.render(self.screen)
            self.render()
            self.all_sprites.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(fps)

    def render(self):
        self.all_sprites = pygame.sprite.Group()
        for i in range(self.board.width):
            for j in range(self.board.height):
                if self.chess.cell(i, j) != '  ':
                    figure = pygame.sprite.Sprite(self.all_sprites)
                    figure.image = pygame.transform.scale(self.images[self.chess.cell(i, j)], (self.board.cell_size - 5, self.board.cell_size - 5))
                    figure.rect = figure.image.get_rect()
                    figure.rect.center = self.board.left + int(self.board.cell_size * (j + 0.5)), \
                                         self.board.left + int(self.board.cell_size * (i + 0.5))

    def opponent(self):
        pass

    def check_mat(self):
        pass

    def finish(self):
        pass
