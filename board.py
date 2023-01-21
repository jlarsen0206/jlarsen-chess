from piece import Piece
import pawn
import rook
import bishop
import knight
import queen
import king
import pygame
from pygame.locals import *
import random


class Board:
    selected_piece = None
    former_ndx = (None, None)
    player = "WHITE"
    move_pos = (None, None)
    check = False
    threatening_piece = None
    orientation = random.randint(0, 1)
    UPPER_COLOR = "WHITE" if orientation == 0 else "BLACK"
    LOWER_COLOR = "WHITE" if orientation != 0 else "BLACK"

    squares = [
        [rook.Rook(UPPER_COLOR), knight.Knight(UPPER_COLOR), bishop.Bishop(UPPER_COLOR), king.King(UPPER_COLOR) if orientation == 0 else queen.Queen(UPPER_COLOR), queen.Queen(
            UPPER_COLOR) if orientation == 0 else king.King(UPPER_COLOR), bishop.Bishop(UPPER_COLOR), knight.Knight(UPPER_COLOR), rook.Rook(UPPER_COLOR)],
        [pawn.Pawn(UPPER_COLOR, 1), pawn.Pawn(UPPER_COLOR, 1), pawn.Pawn(UPPER_COLOR, 1), pawn.Pawn(UPPER_COLOR, 1), pawn.Pawn(
            UPPER_COLOR, 1), pawn.Pawn(UPPER_COLOR, 1), pawn.Pawn(UPPER_COLOR, 1), pawn.Pawn(UPPER_COLOR, 1)],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [pawn.Pawn(LOWER_COLOR, -1), pawn.Pawn(LOWER_COLOR, -1), pawn.Pawn(LOWER_COLOR, -1), pawn.Pawn(LOWER_COLOR, -1), pawn.Pawn(
            LOWER_COLOR, -1), pawn.Pawn(LOWER_COLOR, -1), pawn.Pawn(LOWER_COLOR, -1), pawn.Pawn(LOWER_COLOR, -1)],
        [rook.Rook(LOWER_COLOR), knight.Knight(LOWER_COLOR), bishop.Bishop(LOWER_COLOR), king.King(LOWER_COLOR) if orientation == 0 else queen.Queen(LOWER_COLOR), queen.Queen(
            LOWER_COLOR) if orientation == 0 else king.King(LOWER_COLOR), bishop.Bishop(LOWER_COLOR), knight.Knight(LOWER_COLOR), rook.Rook(LOWER_COLOR)]
    ]

    def update_player(self):
        if self.player == "BLACK":
            self.player = "WHITE"
        elif self.player == "WHITE":
            self.player = "BLACK"

    def get_square(self, piece):
        for i in range(8):
            for j in range(8):
                if isinstance(self.squares[i][j], Piece):
                    if piece == self.squares[i][j]:
                        return (j, i)

    # Return text representation of a piece based on row and col
    def get_piece_text(self, row, col):
        piece = self.squares[row][col]
        result = [None, None]
        if isinstance(piece, Piece):
            if piece.color == "WHITE":
                result[0] = "0"
            if piece.color == "BLACK":
                result[0] = "1"
        if isinstance(piece, pawn.Pawn):
            result[1] = "p"
        if isinstance(piece, knight.Knight):
            result[1] = "n"
        if isinstance(piece, bishop.Bishop):
            result[1] = "b"
        if isinstance(piece, rook.Rook):
            result[1] = "r"
        if isinstance(piece, queen.Queen):
            result[1] = "q"
        if isinstance(piece, king.King):
            result[1] = "k"

        if result != [None, None]:
            return (result[0] + result[1])
        else:
            return None

    def clear_board(self):
        for i in range(8):
            for j in range(8):
                self.squares[i][j] = None

    # Creates a new board, used during a load event
    def construct_board(self, board_text, player, orientation):
        self.clear_board()
        self.player = player
        self.orientation = orientation
        self.UPPER_COLOR = "WHITE" if orientation == 0 else "BLACK"
        self.LOWER_COLOR = "WHITE" if orientation != 0 else "BLACK"

        color = ""
        for i in range(8):
            for j in range(8):
                if board_text[i][j] == None:
                    continue
                elif board_text[i][j] == '':
                    continue
                elif board_text[i][j] == '\n':
                    break

                if board_text[i][j][0] == '0':
                    color = "WHITE"
                elif board_text[i][j][0] == '1':
                    color = "BLACK"

                match board_text[i][j][1]:
                    case "p":
                        if color == self.UPPER_COLOR:
                            self.squares[i][j] = pawn.Pawn(color, 1)
                        else:
                            self.squares[i][j] = pawn.Pawn(color, -1)
                    case "n":
                        self.squares[i][j] = knight.Knight(color)
                    case "b":
                        self.squares[i][j] = bishop.Bishop(color)
                    case "r":
                        self.squares[i][j] = rook.Rook(color)
                    case "q":
                        self.squares[i][j] = queen.Queen(color)
                    case "k":
                        self.squares[i][j] = king.King(color)

    def select_piece(self, piece):
        if (isinstance(piece, Piece)):
            self.selected_piece = piece
            self.former_ndx = self.get_square(piece)

    # Returns clicked piece if a piece is clicked, or None if piece not clicked
    def get_clicked_piece(self):
        pos = pygame.mouse.get_pos()
        # Click outside of board
        if (pos[0] > 799):
            return (-1, -1)
        x = pos[0] // 100
        y = pos[1] // 100
        self.move_pos = (x, y)
        return self.squares[y][x]

    # Move the selected piece to the open square at coordinates (end_x, end_y)
    def move_to_open(self, end_x, end_y):
        piece = self.squares[end_y][end_x]
        if (self.selected_piece and piece == None and self.selected_piece.valid_move(self.former_ndx[0], self.former_ndx[1], end_x, end_y, self.squares)):
            if isinstance(self.selected_piece, pawn.Pawn):
                self.selected_piece.taken_firstmove = True
            temp = self.squares[self.move_pos[1]][self.move_pos[0]]
            self.squares[self.move_pos[1]
                         ][self.move_pos[0]] = self.selected_piece
            self.squares[self.former_ndx[1]][self.former_ndx[0]] = None
            if self.check_for_check(self.player):
                self.squares[self.former_ndx[1]][self.former_ndx[0]
                                                 ] = self.squares[self.move_pos[1]][self.move_pos[0]]
                self.squares[self.move_pos[1]][self.move_pos[0]] = temp
                self.set_reselect()
                return
            self.set_reselect()
            self.update_player()

    # Attempt to capture a piece. Precondition: Colors of selected_piece and to_be_taken are different
    def capture(self, to_be_taken):
        to_be_taken_coords = self.get_square(to_be_taken)
        if (self.selected_piece and isinstance(to_be_taken, Piece) and self.selected_piece.valid_capture(self.former_ndx[0], self.former_ndx[1], to_be_taken_coords[0], to_be_taken_coords[1], self.squares)):
            temp = self.squares[self.move_pos[1]][self.move_pos[0]]
            self.squares[self.move_pos[1]][self.move_pos[0]
                                           ] = self.squares[self.former_ndx[1]][self.former_ndx[0]]
            self.squares[self.former_ndx[1]][self.former_ndx[0]] = None
            if self.check_for_check(self.player):
                self.squares[self.former_ndx[1]][self.former_ndx[0]
                                                 ] = self.squares[self.move_pos[1]][self.move_pos[0]]
                self.squares[self.move_pos[1]][self.move_pos[0]] = temp
                self.set_reselect()
                return
            self.set_reselect()
            self.update_player()

    # Reselect piece when same color piece clicked
    def set_reselect(self):
        self.selected_piece = None
        self.former_ndx = None
        self.move_pos = None

    # Check for checks: get index of King as tuple, iterate through list of pieces potential moves (tuples) to determine
    # if they can kill the king
    # Determines whether this player is in check
    # Can also specify prospective coordinates for a king move to determine whether or not it results in check
    def check_for_check(self, player, this_king=(None, None)):
        prospective_flag = False
        if this_king == (None, None):
            for i in range(8):
                for j in range(8):
                    square = self.squares[i][j]
                    if isinstance(square, king.King) and square.color == player:
                        this_king = (j, i)
        else:
            prospective_flag = True

        for i in range(8):
            for j in range(8):
                to_take = self.squares[i][j]
                if this_king != (None, None):
                    if isinstance(to_take, Piece) and to_take.color != player:
                        if (to_take.valid_capture(j, i, this_king[0], this_king[1], self.squares)):
                            if not prospective_flag:
                                self.check = True
                                self.threatening_piece = to_take
                            return True

        if not prospective_flag:
            self.check = False
            self.threatening_piece = None
        return False

    # Check for and handle rank advancement. TODO: Give user an option of which piece to convert to
    def check_for_promotions(self):
        for i in range(8):
            if (isinstance(self.squares[0][i], pawn.Pawn)):
                self.squares[0][i] = queen.Queen(self.LOWER_COLOR)
            if (isinstance(self.squares[7][i], pawn.Pawn)):
                self.squares[7][i] = queen.Queen(self.UPPER_COLOR)

    # Castling kingside. Precondition: castling is a valid move based solely on board positioning
    def castle_kingside(self):
        if self.check:
            return

        if self.player == self.UPPER_COLOR:
            row = 0
        else:
            row = 7

        self.squares[1][row] = self.squares[0][row]
        self.squares[0][row] = None
        self.squares[2][row] = self.squares[3][row]
        self.squares[3][row] = None

        if (self.check_for_check()):
            self.squares[0][row] = self.squares[1][row]
            self.squares[1][row] = None
            self.squares[3][row] = self.squares[2][row]
            self.squares[2][row] = None
            self.set_reselect()
            return

        self.update_player()

    # Castling queenside. Precondition: castling is a valid move based solely on board positioning
    def castle_queenside(self):
        if self.check:
            return

        if self.player == self.UPPER_COLOR:
            row = 0
        else:
            row = 7

        self.squares[5][row] = self.squares[7][row]
        self.squares[7][row] = None
        self.squares[6][row] = self.squares[4][row]
        self.squares[4][row] = None

        if (self.check_for_check()):
            self.squares[7][row] = self.squares[5][row]
            self.squares[5][row] = None
            self.squares[4][row] = self.squares[6][row]
            self.squares[6][row] = None
            self.set_reselect()
            return

        self.update_player()

    # Return a list of possible move coordinates
    # To be used to evaluate check/checkmate
    def possible_moves(self, piece):
        moves = []
        if isinstance(piece, Piece):
            pos = self.get_square(piece)
        for i in range(8):
            for j in range(8):
                if (piece.valid_move(pos[0], pos[1], i, j, self.squares) and self.squares[j][i] == None):
                    moves.append((i, j))
                elif (piece.valid_capture(pos[0], pos[1], i, j, self.squares) and isinstance(self.squares[j][i], Piece) and self.squares[j][i].color != self.player):
                    moves.append((i, j))
        return moves

    def check_for_mate(self):
        if not self.check:
            return False

        # Check if king can move out of check (also accounts for king captures since king captures the same way as it moves)
        king_total_moves = []
        this_king = (None, None)
        for i in range(8):
            for j in range(8):
                prospective = self.squares[i][j]
                if isinstance(prospective, king.King) and self.player == prospective.color:
                    king_total_moves = self.possible_moves(prospective)
                    this_king = (j, i)

        king_safe_moves = []
        for i in range(len(king_total_moves)):
            if not self.check_for_check(self.player, (king_total_moves[i][0], king_total_moves[i][1])):
                king_safe_moves.append(king_total_moves[i])

        if len(king_safe_moves) != 0:
            return False

        # Check for capturing threatening piece
        threatening_coords = self.get_square(self.threatening_piece)
        for i in range(8):
            for j in range(8):
                if isinstance(self.squares[i][j], Piece) and self.squares[i][j].color == self.player and (not isinstance(self.squares[i][j], king.King)):
                    if (self.squares[i][j].valid_capture(j, i, threatening_coords[0], threatening_coords[1], self.squares)):
                        return False

        # Check for blocks
        if (isinstance(self.threatening_piece, bishop.Bishop) or isinstance(self.threatening_piece, queen.Queen) or isinstance(self.threatening_piece, queen.Queen)):

            path = self.threatening_piece.move_path(
                threatening_coords[0], threatening_coords[1], this_king[0], this_king[1])

            for space in path:
                for i in range(8):
                    for j in range(8):
                        if isinstance(self.squares[i][j], Piece) and self.squares[i][j].color == self.player:
                            if (self.squares[i][j].valid_move(j, i, space[0], space[1], self.squares)):
                                return False

        return True

    #Not used in-game yet due to font rendering incompatibility
    def compute_points(self, player):
        points = 0
        for i in range(8):
            for j in range(8):
                piece = self.squares[i][j]
                if isinstance(piece, pawn.Pawn):
                    points += 1
                elif isinstance(piece, knight.Knight):
                    points += 3
                elif isinstance(piece, bishop.Bishop):
                    points += 3
                elif isinstance(piece, rook.Rook):
                    points += 5
                elif isinstance(piece, queen.Queen):
                    points += 9

        return points
