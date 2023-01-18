import piece
import pygame


class Rook(piece.Piece):
    img = ""
    color = ""

    def __init__(self, color):
        super().__init__(color)
        if (color == "WHITE"):
            self.img = "images/Chess_rlt45.svg.png"
            self.color = color
        else:
            self.img = "images/Chess_rdt45.svg.png"
            self.color = color

    def draw(self):
        return pygame.image.load(self.img).convert_alpha()

    def get_from_board(self, board):
        for i in range(8):
            for j in range(8):
                if board[i][j] == self:
                    return (j, i)

    def move_path(self, start_x, start_y, end_x, end_y):
        for i in [start_x, start_y, end_x, end_y]:
            if i < 0 or i > 7:
                return False
        x_dir = 1 if (end_x > start_x) else -1
        y_dir = 1 if (end_y > start_y) else -1
        path = []

        if (end_x == start_x) ^ (end_y == start_y):
            if (end_x == start_x):
                for i in range(abs(end_y - start_y)):
                    if i == 0:
                        continue
                    path.append((start_x, start_y + (y_dir * i)))
                return path

            elif (end_y == start_y):
                for i in range(abs(end_x - start_x)):
                    if i == 0:
                        continue
                    path.append((start_x + (x_dir * i), start_y))
                return path

        return False

    def valid_move(self, start_x, start_y, end_x, end_y, board):
        for i in [start_x, start_y, end_x, end_y]:
            if i < 0 or i > 7:
                return False
        if (end_x == start_x) ^ (end_y == start_y):
            x_dir = 1 if (end_x > start_x) else -1
            y_dir = 1 if (end_y > start_y) else -1

            coords = self.get_from_board(board)

            if ((end_x == start_x) ^ (end_y == start_y)):
                if (end_x == start_x):
                    for i in range(abs(end_y - start_y)):
                        if i == 0:
                            continue
                        if isinstance(board[y_dir * i + coords[1]][coords[0]], piece.Piece):
                            return False
                elif (end_y == start_y):
                    for i in range(abs(end_x - start_x)):
                        if i == 0:
                            continue
                        if isinstance(board[coords[1]][x_dir * i + coords[0]], piece.Piece):
                            return False
                return True
        return False

    def valid_capture(self, start_x, start_y, end_x, end_y, board):
        return self.valid_move(start_x, start_y, end_x, end_y, board)
