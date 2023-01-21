import board
import evaluate
import piece
from piece import Piece
from pawn import Pawn
from knight import Knight
from bishop import Bishop
from rook import Rook
from queen import Queen
from king import King
from board import Board
import random


class Opponent():
    color = ""
    board = None
    
    def __init__(self, color, board):
        self.color = color
        if isinstance(board, Board):
            self.board = board

    def best_move(self):
        this_status = evaluate.evaluate(board)
        moves = []
        for i in range(8):
            for j in range(8):
                if isinstance(self.board.squares[i][j], Piece) and self.board.squares[i][j].color == self.color:
                    moves.extend(self.board.possible_moves(self.board.squares[i][j]))

        prospective_board = None
        best_eval = this_status
        best = (None, None)

        for move in moves:
            prospective_board = board.Board()
            prospective_board.squares = self.board.squares
            
            if self.board.squares[move[1]][move[0]] != None:
                prospective_board.capture(prospective_board.get_square((move[1],move[0])))
            else:
                prospective_board.move_to_open(move[0], move[1])

            this_eval = evaluate.evaluate(prospective_board)

            if self.color == "WHITE":
                if this_eval > best_eval:
                    best_eval = this_eval
                    best = move
            else:
                if this_eval < best_eval:
                    best_eval = this_eval
                    best = move

        if best != (None, None):
            return best
        else:
            size = len(moves)
            ndx = random.randint(0, size)
            return moves[ndx]

        