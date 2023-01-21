import board
import piece
from piece import Piece
from pawn import Pawn
from knight import Knight
from bishop import Bishop
from rook import Rook
from queen import Queen
from king import King
from board import Board

def evaluate(board):
    diff = 0
    if isinstance(board, Board):
        diff = board.compute_points("WHITE") - board.compute_points("BLACK")

    return diff
