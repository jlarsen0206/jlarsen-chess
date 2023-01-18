import piece
import pygame


class Knight(piece.Piece):
    img = ""
    color = ""

    def __init__(self, color):
        super().__init__(color)
        if (color == "WHITE"):
            self.img = "images/Chess_nlt45.svg.png"
            self.color = color
        else:
            self.img = "images/Chess_ndt45.svg.png"
            self.color = color

    def draw(self):
        return pygame.image.load(self.img).convert_alpha()

    def valid_move(self, start_x, start_y, end_x, end_y, board):
        for i in [start_x, start_y, end_x, end_y]:
            if i < 0 or i > 7:
                return False
        if (abs(end_x - start_x) == 1):
            if (abs(end_y - start_y) == 2):
                return True
        if (abs(end_x - start_x) == 2):
            if (abs(end_y - start_y) == 1):
                return True
        return False

    def valid_capture(self, start_x, start_y, end_x, end_y, board):
        return self.valid_move(start_x, start_y, end_x, end_y, board)
