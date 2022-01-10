WHITE = 1
BLACK = 2


# Удобная функция для вычисления цвета противника
def opponent(color):
    if color == WHITE:
        return BLACK
    else:
        return WHITE


def print_board(board):  # Распечатать доску в текстовом виде (см. скриншот)
    print('     +----+----+----+----+----+----+----+----+')
    for row in range(7, -1, -1):
        print(' ', row, end='  ')
        for col in range(8):
            print('|', board.cell(row, col), end=' ')
        print('|')
        print('     +----+----+----+----+----+----+----+----+')
    print(end='        ')
    for col in range(8):
        print(col, end='    ')
    print()



def check_mat(board):
    now = [[j for j in i] for i in board.field]
    for i in range(8):
        for j in range(8):
            fig = board.get_piece(i, j)
            if fig is not None and fig.color == board.color:
                for i1 in range(8):
                    for j1 in range(8):
                        if board.move_piece1(i, j, i1, j1):
                            board.field = [[kk for kk in k] for k in now]
                            return False
                        board.field = [[kk for kk in k] for k in now]
    return True


def main():
    # Создаём шахматную доску
    board = Board()
    # Цикл ввода команд игроков
    # print_board(board)
    while True:
        board.NUM += 1
        if board.current_player_color() == WHITE:
            print('Ход белых:')
        else:
            print('Ход чёрных:')
        command = input()
        if command.split()[0] == 'help':
            for i in range(10):
                print()
            help(command.split()[1])
        elif command == 'exit':
            break
        elif command == 'board':
            print_board(board)
        elif command == 'leave':
            x = 'Белые' if board.color == BLACK else 'Черные'
            print(x, 'выиграли!')
            com = ''
            while com != 'exit' and com != 'new':
                print('Команды:')
                print('        exit            -- выход')
                print('        new             -- начать новую партию')
                com = input()
            if com == 'exit':
                break
            board = Board()
            print_board(board)
        else:
            if not (len(command.split()) == 5 and command.split()[0] == 'move'):
                print('Неверный ввод, попробуйте еще раз')
                continue
            for i in range(10):
                print()
            move_type, row, col, row1, col1 = command.split()
            row, col, row1, col1 = int(row), int(col), int(row1), int(col1)
            if board.move_piece(row, col, row1, col1):
                print('Ход успешен')
            else:
                print('Координаты некорректы! Попробуйте другой ход!')
            print_board(board)
            x, y = 0, 0
            for i in range(8):
                for j in range(8):
                    if type(board.field[i][j]) is King and board.field[i][j].color == board.color:
                        x, y = i, j
            if check_mat(board):
                if board.is_under_attack(x, y, board.color):
                    x = 'белые' if board.color == BLACK else 'черные'
                    print('Мат! {} выиграли!'.format(x))
                else:
                    print('Увы, пат!')
                com = ''
                while com != 'exit' and com != 'new':
                    print('Команды:')
                    print('        exit            -- выход')
                    print('        new             -- начать новую партию')
                    com = input()
                if com == 'exit':
                    break
                board = Board()
                print_board(board)


def correct_coords(row, col):
    return 0 <= row < 8 and 0 <= col < 8


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
            Pawn(BLACK), Pawn(WHITE), Pawn(BLACK), Pawn(BLACK),
            Pawn(BLACK), Pawn(BLACK), Pawn(BLACK), Pawn(BLACK)
        ]
        self.field[7] = [
            Rook(BLACK), None, Bishop(BLACK), Queen(BLACK),
            King(BLACK), Bishop(BLACK), Knight(BLACK), Rook(BLACK)
        ]

    def current_player_color(self):
        return self.color

    def is_under_attack(self, row, col, color):
        for i in range(8):
            for j in range(8):
                if (self.field[i][j] is not None and
                        (i != row or j != col) and
                        self.field[i][j].color != color and
                        self.field[i][j].can_attack(self, i, j, row, col)):
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
        if correct_coords(row, col):
            return self.field[row][col]
        else:
            return None

    def move_piece1(self, row, col, row1, col1):  # похожая ф-ия для проверки мата
        pred = [[j for j in i] for i in self.field]
        if not correct_coords(row, col) or not correct_coords(row1, col1):
            return False
        if row == row1 and col == col1:
            return False  # нельзя пойти в ту же клетку
        piece = self.field[row][col]
        if piece is None:
            return False
        if self.field[row1][col1] is None:
            if not piece.can_move(self, row, col, row1, col1):
                return False
        elif self.field[row1][col1].get_color() == opponent(piece.get_color()):
            if not piece.can_attack(self, row, col, row1, col1):
                return False
        else:
            return False
        self.field[row][col] = None  # Снять фигуру.
        self.field[row1][col1] = piece  # Поставить на новое место.
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
        return True

    def move_piece(self, row, col, row1, col1):
        pred = [[j for j in i] for i in self.field]
        if not correct_coords(row, col) or not correct_coords(row1, col1):
            print('Координаты за пределами поля!')
            return False
        if row == row1 and col == col1:
            print('Нельзя пойти в ту же клетку!')
            return False  # нельзя пойти в ту же клетку
        piece = self.field[row][col]
        if piece is None:
            print('Там нет фигуры!')
            return False
        if piece.get_color() != self.color:
            x = 'белых' if self.color == WHITE else 'черных'
            print('Сейчас ход {}!'.format(x))
            return False
        if self.field[row1][col1] is None:
            if not piece.can_move(self, row, col, row1, col1):
                print('Эта фигура не может так ходить!')
                return False
        elif self.field[row1][col1].get_color() == opponent(piece.get_color()):
            if not piece.can_attack(self, row, col, row1, col1):
                print('Эта фигура не может так ходить!')
                return False
        else:
            print('Нельзя бить своих!')
            return False
        self.field[row][col] = None  # Снять фигуру.
        self.field[row1][col1] = piece  # Поставить на новое место.
        x, y = 0, 0
        for i in range(8):
            for j in range(8):
                p = self.get_piece(i, j)
                if type(p) is King and p.color == self.color:
                    x, y = i, j
                    break
        if self.is_under_attack(x, y, self.color):
            self.field = pred[:]
            print('Вам шах!')
            return False
        # x = 7 if self.color == WHITE else 0
        # if row1 == x and type(self.get_piece(row1, col1)) is Pawn:
        #     print("Выберите фигуру, где N - конь, B - слон, R - Ладья и Q - ферзь:")
        #     le = input()
        #     if le == "N":
        #         self.field[row1][col1] = Knight(self.color)
        #     elif le == "B":
        #         self.field[row1][col1] = Bishop(self.color)
        #     elif le == "R":
        #         self.field[row1][col1] = Rook(self.color)
        #     elif le == "Q":
        #         self.field[row1][col1] = Queen(self.color)
        self.color = opponent(self.color)
        return True


class Rook:

    def __init__(self, color):
        self.color = color
        self.flag = 1

    def get_color(self):
        return self.color

    def char(self):
        return 'R'

    def can_move(self, board, row, col, row1, col1):
        if row != row1 and col != col1:
            return False

        step = 1 if (row1 >= row) else -1
        for r in range(row + step, row1, step):
            if not (board.get_piece(r, col) is None):
                return False

        step = 1 if (col1 >= col) else -1
        for c in range(col + step, col1, step):
            # Если на пути по вертикали есть фигура
            if not (board.get_piece(row, c) is None):
                return False

        self.flag = 0
        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Pawn:

    def __init__(self, color):
        self.color = color
        self.flag = 0

    def get_color(self):
        return self.color

    def char(self):
        return 'P'

    def can_move(self, board, row, col, row1, col1):
        # "взятие на проходе" реализовано
        # if col != col1:
        #     direction = 1 if (self.color == WHITE) else -1
        #     # print(board.field[row1 - direction][col1].flag, board.NUM - 1)
        #     if (self.can_attack(board, row, col, row1, col1) and
        #             type(board.field[row1 - direction][col1]) is Pawn and
        #             board.field[row1 - direction][col1].color != self.color):
        #             # board.field[row1 - direction][col1].flag == board.NUM):
        #         board.field[row1 - direction][col1] = None
        #         print(1)
        #         return True
        #     return False

        # Пешка может сделать из начального положения ход на 2 клетки
        # вперёд, поэтому поместим индекс начального ряда в start_row.
        if self.color == WHITE:
            direction = 1
            start_row = 1
        else:
            direction = -1
            start_row = 6

        # ход на 1 клетку
        if row + direction == row1:
            return True

        # ход на 2 клетки из начального положения
        if (row == start_row
                and row + 2 * direction == row1
                and board.field[row + direction][col] is None):
            self.flag = board.NUM
            return True

        return False

    def can_attack(self, board, row, col, row1, col1):
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
        return 'N'  # kNight, буква 'K' уже занята королём

    def can_move(self, board, row, col, row1, col1):
        return abs(row - row1) * abs(col - col1) == 2

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class King:
    def __init__(self, color):
        self.color = color
        self.flag = 1

    def get_color(self):
        return self.color

    def char(self):
        return 'K'

    def can_move(self, board, row, col, row1, col1):
        if (abs(row - row1) <= 1 and abs(col - col1) <= 1 and
                not board.is_under_attack(row1, col1, self.color)):
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
            board.move_piece(7, 0, 7, 3)
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
            board.move_piece(7, 7, 7, 5)
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
            board.move_piece(0, 0, 0, 3)
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
            board.move_piece(0, 7, 0, 5)
            return True
        return False

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Queen:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'Q'

    def can_move(self, board, row, col, row1, col1):
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
            # Если на пути по горизонтали есть фигура
            if not (board.get_piece(r, col) is None):
                return False

        step = 1 if (col1 >= col) else -1
        for c in range(col + step, col1, step):
            # Если на пути по вертикали есть фигура
            if not (board.get_piece(row, c) is None):
                return False

        return True

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


class Bishop:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color

    def char(self):
        return 'B'

    def can_move(self, board, row, col, row1, col1):
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

    def can_attack(self, board, row, col, row1, col1):
        return self.can_move(board, row, col, row1, col1)


if __name__ == "__main__":
    main()