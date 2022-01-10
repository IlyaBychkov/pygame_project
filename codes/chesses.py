WHITE = 1
BLACK = 2


class Board:
    def __init__(self, width=8, height=8, left=10, top=10, cell_size=10, width_frame=2):
        self.NUM = 0
        self.width = width
        self.height = height
        self.left = left
        self.top = top
        self.cell_size = cell_size
        self.width_frame = width_frame
        self.color = WHITE
        self.field = []
        for row in range(8):
            self.field.append([None] * 8)
        self.field[0] = [
            Rook(WHITE), Knight(WHITE), Bishop(WHITE), Queen(WHITE),
            King(WHITE), Bishop(WHITE), Knight(WHITE), Rook(WHITE)
        ]
        self.field[1] = [
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE),
            Pawn(WHITE), Pawn(WHITE), Pawn(WHITE), Pawn(WHITE)
        ]
        self.field[6] = [
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK),
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK)
        ]
        self.field[7] = [
            Rook(BLACK), Knight(BLACK), Bishop(BLACK), Queen(BLACK),
            King(BLACK), Bishop(BLACK), Knight(BLACK), Rook(BLACK)
        ]
        # self.field[7][4] = King(BLACK)
        # self.field[0][4] = King(WHITE)
        # self.field[0][7] = Rook(WHITE)

    def get_coords(self, x, y):
        return (self.left + int(self.cell_size * (y + 0.5)), self.left + int(
            self.cell_size * (7 - x + 0.5)))

    def is_under_attack(self, row, col, color):
        for i in range(8):
            for j in range(8):
                if (self.field[i][j] is not None and
                        (i != row or j != col) and
                        self.field[i][j].color != color and
                        self.field[i][j].can_attack(self, i, j, row, col, 0)):
                    return True
        return False

    def cell(self, row, col):
        piece = self.field[row][col]
        if piece is None:
            return '  '
        color = piece.get_color()
        c = 'w' if color == WHITE else 'b'
        return c + piece.char()

    def get_piece(self, row, col):
        return self.field[row][col]

    def move_piece(self, row, col, row1, col1, fl=1):
        pred = [[j for j in i] for i in self.field]
        if row == row1 and col == col1:
            return False
        piece = self.field[row][col]
        if piece is None:
            return False
        if piece.get_color() != self.color:
            return False
        if self.field[row1][col1] is None:
            if not piece.can_move(self, row, col, row1, col1, fl):
                return False
        elif self.field[row1][col1].get_color() == self.opponent(piece.get_color()):
            if not piece.can_attack(self, row, col, row1, col1, fl):
                return False
        else:
            return False
        self.field[row][col] = None
        self.field[row1][col1] = piece
        x, y = 0, 0
        for i in range(8):
            for j in range(8):
                p = self.get_piece(i, j)
                if type(p) is King and p.color == self.color:
                    x, y = i, j
                    break
        if self.is_under_attack(x, y, self.color):
            self.field = pred[:]
            return False
        if fl:
            self.color = self.opponent(self.color)
        else:
            self.field = pred[:]
        return True

    def check_mat(self):
        x, y = -1, -1
        now = [[j for j in i] for i in self.field]
        for i in range(8):
            for j in range(8):
                fig = self.get_piece(i, j)
                if fig is not None and fig.color == self.color:
                    if type(fig) is King:
                        x, y = i, j
                    for i1 in range(8):
                        for j1 in range(8):
                            if self.move_piece(i, j, i1, j1, 0):
                                self.field = [[kk for kk in k] for k in now]
                                return False
                            self.field = [[kk for kk in k] for k in now]
        if self.is_under_attack(x, y, self.color):
            return 1
        return 2

    def opponent(self, color):
        if color == WHITE:
            return BLACK
        else:
            return WHITE

    def print_board(self):  # Распечатать доску в текстовом виде (см. скриншот)
        print('     +----+----+----+----+----+----+----+----+')
        for row in range(7, -1, -1):
            print(' ', row, end='  ')
            for col in range(8):
                print('|', self.cell(row, col), end=' ')
            print('|')
            print('     +----+----+----+----+----+----+----+----+')
        print(end='        ')
        for col in range(8):
            print(col, end='    ')
        print()


class Rook:
    def __init__(self, color):
        self.color = color
        self.flag = 1

    def get_color(self):
        return self.color

    def char(self):
        return 'R'

    def can_move(self, board, row, col, row1, col1, fl=1):
        if row != row1 and col != col1:
            return False

        step = 1 if (row1 >= row) else -1
        for r in range(row + step, row1, step):
            if not (board.get_piece(r, col) is None):
                return False

        step = 1 if (col1 >= col) else -1
        for c in range(col + step, col1, step):
            if not (board.get_piece(row, c) is None):
                return False
        if fl:
            self.flag = 0
        return True

    def can_attack(self, board, row, col, row1, col1, fl=1):
        return self.can_move(board, row, col, row1, col1, fl)


class Pawn:
    def __init__(self, color):
        self.color = color
        self.flag = 0

    def get_color(self):
        return self.color

    def char(self):
        return 'P'

    def can_move(self, board, row, col, row1, col1, fl=1):
        if col != col1:
            direction = 1 if (self.color == WHITE) else -1
            if (self.can_attack(board, row, col, row1, col1, fl) and
                    type(board.field[row1 - direction][col1]) is Pawn and
                    board.field[row1 - direction][col1].color != self.color and
                    board.field[row1 - direction][col1].flag == board.NUM - 1):
                if fl:
                    board.field[row1 - direction][col1].sprite.kill()
                    board.field[row1 - direction][col1] = None
                return True
            return False

        if self.color == WHITE:
            direction = 1
            start_row = 1
        else:
            direction = -1
            start_row = 6

        if row + direction == row1:
            return True

        if (row == start_row
                and row + 2 * direction == row1
                and board.field[row + direction][col] is None):
            self.flag = board.NUM
            return True

        return False

    def can_attack(self, board, row, col, row1, col1, fl=1):
        direction = 1 if (self.color == WHITE) else -1
        if (row + direction == row1
                and (col + 1 == col1 or col - 1 == col1)):
            return True
        return False


class Knight:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'N'

    def can_move(self, board, row, col, row1, col1, fl=1):
        return abs(row - row1) * abs(col - col1) == 2

    def can_attack(self, board, row, col, row1, col1, fl=1):
        return self.can_move(board, row, col, row1, col1, fl)


class King:
    def __init__(self, color):
        self.color = color
        self.flag = 1

    def get_color(self):
        return self.color

    def char(self):
        return 'K'

    def can_move(self, board, row, col, row1, col1, fl=1):
        if (abs(row - row1) <= 1 and abs(col - col1) <= 1 and
                not board.is_under_attack(row1, col1, self.color)):
            if fl:
                self.flag = 0
            return True

        fig = board.get_piece(7, 0)
        if (row == row1 == 7 and col - 2 == col1 == 2 and
                self.flag and type(fig) is Rook and
                fig.color == self.color == BLACK and
                fig.flag):
            for i in range(1, 4):
                if board.get_piece(7, i) is not None:
                    return False
            for i in range(2, 5):
                if board.is_under_attack(7, i, self.color):
                    return False
            if fl:
                board.field[7][0].sprite.rect.center = board.get_coords(7, 3)
                board.move_piece(7, 0, 7, 3)
                board.color = board.opponent(board.color)
            return True

        fig = board.get_piece(7, 7)
        if (row == row1 == 7 and col + 2 == col1 == 6 and
                self.flag and type(fig) is Rook and
                fig.color == self.color == BLACK and
                fig.flag):
            for i in range(6, 4, -1):
                if board.get_piece(7, i) is not None:
                    return False
            for i in range(6, 3, -1):
                if board.is_under_attack(7, i, self.color):
                    return False
            if fl:
                board.field[7][7].sprite.rect.center = board.get_coords(7, 5)
                board.move_piece(7, 7, 7, 5)
                board.color = board.opponent(board.color)
            return True

        fig = board.get_piece(0, 0)
        if (row == row1 == 0 and col - 2 == col1 == 2 and
                self.flag and type(fig) is Rook and
                fig.color == self.color == WHITE and
                fig.flag):
            for i in range(1, 4):
                if board.get_piece(0, i) is not None:
                    return False
            for i in range(2, 5):
                if board.is_under_attack(0, i, self.color):
                    return False
            if fl:
                board.field[0][0].sprite.rect.center = board.get_coords(0, 3)
                board.move_piece(0, 0, 0, 3)
                board.color = board.opponent(board.color)
            return True

        fig = board.get_piece(0, 7)
        if (row == row1 == 0 and col + 2 == col1 == 6 and
                self.flag and type(fig) is Rook and
                fig.color == self.color == WHITE and
                fig.flag):
            for i in range(6, 4, -1):
                if board.get_piece(0, i) is not None:
                    return False
            for i in range(6, 3, -1):
                if board.is_under_attack(0, i, self.color):
                    return False
            if fl:
                board.field[0][7].sprite.rect.center = board.get_coords(0, 5)
                board.move_piece(0, 7, 0, 5)
                board.color = board.opponent(board.color)
            return True
        return False

    def can_attack(self, board, row, col, row1, col1, fl=1):
        return self.can_move(board, row, col, row1, col1, fl)


class Queen:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'Q'

    def can_move(self, board, row, col, row1, col1, fl=1):
        i, j = row + 1, col + 1
        while i < 8 and j < 8:
            if i == row1 and j == col1:
                return True
            if board.field[i][j] is None:
                i, j = i + 1, j + 1
            else:
                break
        i, j = row - 1, col + 1
        while i >= 0 and j < 8:
            if i == row1 and j == col1:
                return True
            if board.field[i][j] is None:
                i, j = i - 1, j + 1
            else:
                break
        i, j = row - 1, col - 1
        while i >= 0 and j >= 0:
            if i == row1 and j == col1:
                return True
            if board.field[i][j] is None:
                i, j = i - 1, j - 1
            else:
                break
        i, j = row + 1, col - 1
        while i < 8 and j >= 0:
            if i == row1 and j == col1:
                return True
            if board.field[i][j] is None:
                i, j = i + 1, j - 1
            else:
                break

        if row != row1 and col != col1:
            return False

        step = 1 if (row1 >= row) else -1
        for r in range(row + step, row1, step):
            if not (board.get_piece(r, col) is None):
                return False

        step = 1 if (col1 >= col) else -1
        for c in range(col + step, col1, step):
            if not (board.get_piece(row, c) is None):
                return False

        return True

    def can_attack(self, board, row, col, row1, col1, fl=1):
        return self.can_move(board, row, col, row1, col1, fl)


class Bishop:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'B'

    def can_move(self, board, row, col, row1, col1, fl=1):
        i, j = row + 1, col + 1
        while i < 8 and j < 8:
            if i == row1 and j == col1:
                return True
            if board.field[i][j] is None:
                i, j = i + 1, j + 1
            else:
                break
        i, j = row - 1, col + 1
        while i >= 0 and j < 8:
            if i == row1 and j == col1:
                return True
            if board.field[i][j] is None:
                i, j = i - 1, j + 1
            else:
                break
        i, j = row - 1, col - 1
        while i >= 0 and j >= 0:
            if i == row1 and j == col1:
                return True
            if board.field[i][j] is None:
                i, j = i - 1, j - 1
            else:
                break
        i, j = row + 1, col - 1
        while i < 8 and j >= 0:
            if i == row1 and j == col1:
                return True
            if board.field[i][j] is None:
                i, j = i + 1, j - 1
            else:
                break
        return False

    def can_attack(self, board, row, col, row1, col1, fl=1):
        return self.can_move(board, row, col, row1, col1, fl)