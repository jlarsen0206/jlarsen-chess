import piece
import pygame
import rook


class King(piece.Piece):
    img = ""
    color = ""

    def __init__(self, color):
        super().__init__(color)
        if (color == "WHITE"):
            self.img = "images/Chess_klt45.svg.png"
            self.color = color
        else:
            self.img = "images/Chess_kdt45.svg.png"
            self.color = color

    def draw(self):
        return pygame.image.load(self.img).convert_alpha()

    def valid_move(self, start_x, start_y, end_x, end_y, board):
        for i in [start_x, start_y, end_x, end_y]:
            if i < 0 or i > 7:
                return False
        if abs(end_x - start_x) <= 1 and abs(end_y - start_y) <= 1:
            return True
        return False

    def valid_capture(self, start_x, start_y, end_x, end_y, board):
        return self.valid_move(start_x, start_y, end_x, end_y, board)

    def can_castle_kingside(self, board):
        king = (None, None)
        x = 3
        if (self.color == "WHITE"):
            y = 0
        else:
            y = 7
        prospective_king = board[y][x]
        if isinstance(prospective_king, King) and prospective_king.color == self.color:
            if (board[y][2] == None) and (board[y][1] == None):
                if isinstance(board[y][0], rook.Rook) and board[y][0].color == self.color:
                    return True
        return False

    def can_castle_queenside(self, board):
        king = (None, None)
        x = 3
        if (self.color == "WHITE"):
            y = 0
        else:
            y = 7
        prospective_king = board[y][x]
        if isinstance(prospective_king, King) and prospective_king.color == self.color:
            if (board[y][4] == None) and (board[y][5] == None) and (board[y][6] == None):
                if isinstance(board[y][7], rook.Rook) and board[y][7].color == self.color:
                    return True
        return False
