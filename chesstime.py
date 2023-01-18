
import board
import pygame


class ChessTime():

    init_time = 0
    white_time = 600000
    black_time = 600000

    def __init__(self, white_time, black_time):
        self.white_time = white_time
        self.black_time = black_time

    def start(self):
        self.init_time = pygame.time.get_ticks()

    def compute_time(self, player):
        final_time = pygame.time.get_ticks()

        if (player == "WHITE"):
            self.white_time -= (final_time - self.init_time)

        elif (player == "BLACK"):
            self.black_time -= (final_time - self.init_time)
            self.start()

    def display_time(self, player):

        if player == "WHITE":
            this_time = self.white_time
        else:
            this_time = self.black_time

        this_time = this_time / 60000
        font = pygame.font.Font(None, 32)
        font.render(str(this_time), True, (255, 255, 255))
        font_surface = pygame.rect(font)
