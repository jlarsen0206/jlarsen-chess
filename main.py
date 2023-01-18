import pygame
from pygame.locals import *
import sys
from piece import Piece
from pawn import Pawn
from knight import Knight
from bishop import Bishop
from rook import Rook
from queen import Queen
from king import King
from board import Board
from handleSaveLoad import HandleCSV
from chesstime import ChessTime

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chess")
icon = pygame.image.load("images/chess_icon-icons.com_65163.png")
pygame.display.set_icon(icon)
board = Board()
game_running = False

clock = ChessTime(600000, 600000)
clock.start()


def draw():
    draw_board(board.squares)
    handle_selected_piece()
    board.check_for_promotions()
    board.check_for_check(board.player)
    handle_check(board.player)
    draw_pieces()
    board.check_for_mate()
    # display_time()


def draw_board(squares):
    square_size = SCREEN_HEIGHT // 8
    # White Squares
    for x in range(0, 8, 2):
        for y in range(0, 8, 2):
            pygame.draw.rect(screen, (255, 255, 255), (x*square_size,
                             y*square_size, square_size, square_size))
    for x in range(1, 8, 2):
        for y in range(1, 8, 2):
            pygame.draw.rect(screen, (255, 255, 255), (x*square_size,
                             y*square_size, square_size, square_size))

    # Black squares
    for x in range(1, 8, 2):
        for y in range(0, 8, 2):
            pygame.draw.rect(screen, (51, 25, 0), (x*square_size,
                             y*square_size, square_size, square_size))
    for x in range(0, 8, 2):
        for y in range(1, 8, 2):
            pygame.draw.rect(screen, (51, 25, 0), (x*square_size,
                             y*square_size, square_size, square_size))


def draw_pieces():
    for j in range(8):
        i = 0
        while i < 8:
            if board.squares[j][i] != None:
                piece = board.squares[j][i]
                if isinstance(piece, Piece):
                    if (board.selected_piece == None or not (piece is board.selected_piece)):
                        screen.blit(piece.draw(), (i*100, j * 100))
            i = i + 1


def handle_selected_piece():
    if board.selected_piece:
        square = board.get_square(board.selected_piece)
        if square != None:
            pygame.draw.rect(screen, (239, 247, 2),
                             (square[0] * 100, square[1] * 100, 100, 100))
            for move in board.possible_moves(board.selected_piece):
                pygame.draw.circle(screen, (239, 247, 2),
                                   (move[0] * 100 + 50, move[1] * 100 + 50), 15)

            # Follow cursor
            mouse_pos = pygame.mouse.get_pos()
            screen.blit(board.selected_piece.draw(),
                        (mouse_pos[0] - 50, mouse_pos[1] - 50))


def handle_check(player):
    for i in range(8):
        for j in range(8):
            prospective_in_check = board.squares[i][j]
            if (isinstance(prospective_in_check, King) and board.check_for_check(player)):
                if (prospective_in_check.color == player):
                    pygame.draw.rect(screen, (236, 0, 0),
                                     (j * 100, i * 100, 100, 100))

# Displays time for each player. Text rendering in pygame is not compatible with MacOS M1
# Time constraints not implemented in game loop since time is not visible


def display_time():
    screen.blit(clock.display_time("WHITE"), dest=(
        (800, 100) if board.UPPER_COLOR == "WHITE" else (800, 700)))
    screen.blit(clock.display_time("BLACK"), dest=(
        (800, 700) if board.UPPER_COLOR == "WHITE" else (800, 100)))

# TODO


def handle_checkmate(player):
    pass

# TODO: figure out how to render text for buttons, time, rect


def chess():

    global board
    global game_running

    if game_running == False:
        return

    draw()

    pygame.display.flip()

    for event in pygame.event.get():

        if event.type == KEYDOWN:

            if event.key == K_ESCAPE:
                game_running = False

            # Save: write to database.csv
            elif event.key == K_s:
                file = HandleCSV('board.csv')
                file.handle_save(board)

        elif event.type == QUIT:
            sys.exit()

        elif event.type == MOUSEBUTTONDOWN:

            clicked = board.get_clicked_piece()

            # Click outside of board
            if (clicked == (-1, -1)):
                continue

            clicked_coords = board.move_pos

            if not board.selected_piece and isinstance(clicked, Piece) and board.player == clicked.color:
                board.select_piece(clicked)

            elif not board.selected_piece and isinstance(clicked, Piece) and board.player != clicked.color:

                board.set_reselect()

            else:
                # Case: Move to open square
                if clicked == None:

                    board.move_to_open(clicked_coords[0], clicked_coords[1])

                    clock.compute_time(board.player)

                elif isinstance(clicked, Piece) and clicked.color != board.player:

                    board.capture(clicked)

                    clock.compute_time(board.player)

                elif isinstance(clicked, Piece) and clicked.color == board.player:

                    if isinstance(board.selected_piece, King) and isinstance(clicked, Rook):

                        if board.selected_piece.can_castle_kingside() and (clicked_coords == (0, 0) or clicked_coords == (7, 0)):
                            board.castle_kingside()

                        elif board.selected_piece.can_castle_queenside() and clicked_coords == (7, 0) or clicked_coords == (7, 7):
                            board.castle_queenside()

                    board.set_reselect()


def main_menu():
    global game_running
    background_color = (43, 42, 39)
    rect_height = SCREEN_HEIGHT // 10
    rect_width = SCREEN_WIDTH // 5

    while True:

        if game_running:
            break
        else:
            screen.fill(background_color)

            pygame.draw.rect(screen, (235, 233, 228), (SCREEN_WIDTH // 2 - rect_width // 2, SCREEN_HEIGHT //
                             2 - rect_height - 60, rect_width, rect_height), border_radius=rect_width // 14)
            pygame.draw.rect(screen, (235, 233, 228), (SCREEN_WIDTH // 2 - rect_width // 2, SCREEN_HEIGHT //
                             2 - rect_height // 2, rect_width, rect_height), border_radius=rect_width // 14)
            pygame.draw.rect(screen, (235, 233, 228), (SCREEN_WIDTH // 2 - rect_width // 2, SCREEN_HEIGHT //
                             2 + rect_height // 2 + 20, rect_width, rect_height), border_radius=rect_width // 14)
            screen.blit(pygame.image.load(
                'images/play_green_button_icon_227849-2.png'), (SCREEN_WIDTH // 2 - 32, SCREEN_HEIGHT //
                                                                2 - rect_height - 60 + 8, rect_width, rect_height))
            screen.blit(pygame.image.load(
                'images/application_software_office_loadcenter_charged_1856.png'), (SCREEN_WIDTH // 2 - 32, SCREEN_HEIGHT //
                                                                                    2 - 32, rect_width, rect_height))
            screen.blit(pygame.image.load(
                'images/remove_delete_exit_close_1545.png'), (SCREEN_WIDTH // 2 - 32, SCREEN_HEIGHT //
                                                              2 + rect_height - 12, rect_width, rect_height))
            pygame.display.flip()

            for event in pygame.event.get():

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()

                elif event.type == QUIT:
                    pygame.quit()

                elif event.type == MOUSEBUTTONDOWN:
                    clicked_pos = pygame.mouse.get_pos()

                    if (clicked_pos[0] > SCREEN_WIDTH // 2 - rect_width // 2 and clicked_pos[0] < SCREEN_WIDTH // 2 - rect_width // 2 + rect_width):

                        if (clicked_pos[1] > (SCREEN_HEIGHT // 2 - rect_height - 60) and clicked_pos[1] < (SCREEN_HEIGHT // 2 - rect_height - 60 + rect_height)):
                            # Play button
                            game_running = True

                        elif (clicked_pos[1] > (SCREEN_HEIGHT // 2 - rect_height // 2) and clicked_pos[1] < (SCREEN_HEIGHT // 2 - rect_height // 2 + rect_height)):
                            # Load button click
                            file = HandleCSV('board.csv')
                            file.handle_load(board)
                            game_running = True

                        elif (clicked_pos[1] > (SCREEN_HEIGHT // 2 + rect_height // 2 + 20) and (clicked_pos[1] < SCREEN_HEIGHT // 2 + rect_height // 2 + 20 + rect_height)):
                            # Quit button
                            sys.exit()


# Main game loop
while True:
    if game_running:
        chess()
    else:
        main_menu()
