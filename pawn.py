from asyncio import FastChildWatcher
import piece
import pygame
import math


class Pawn(piece.Piece):
    img = ""
    color = ""
    taken_firstmove = False

    def __init__(self, color):
        super().__init__(color)
        if (color == "WHITE"):
            self.img = "images/Chess_plt45.svg.png"
            self.color = color
        else:
            self.img = "images/Chess_pdt45.svg.png"
            self.color = color

    def draw(self):
        return pygame.image.load(self.img).convert_alpha()

    def valid_move(self, start_x, start_y, end_x, end_y, board):
        for i in [start_x, start_y, end_x, end_y]:
            if i < 0 or i > 7:
                return False
        if end_x == start_x:
            if self.color == "WHITE" and end_y - start_y == 1:
                return True
            if self.color == "BLACK" and end_y - start_y == -1:
                return True
            if not self.taken_firstmove:
                if self.color == "WHITE" and end_y - start_y == 2:
                    return True
                if self.color == "BLACK" and end_y - start_y == -2:
                    return True

        return False

    def valid_capture(self, start_x, start_y, end_x, end_y, board):
        if end_x - start_x == 1 or end_x - start_x == -1:
            if (self.color == "WHITE") and end_y - start_y == 1:
                return True
            if (self.color == "BLACK") and end_y - start_y == -1:
                return True
        return False
