class Piece:
    row = 0
    col = 0
    color = None
    possible_moves = []

    def __init__(self, color):
        self.color = color
    
    @classmethod
    def draw(self):
        pass

    #Checks if a given move is valid
    @classmethod
    def valid_move(self, start_x, start_y, end_x, end_y, board):
        pass

    #Checks if a given capture is valid (ie, account for pawn's different capture behavior)
    @classmethod
    def valid_capture(self, start_x, start_y, end_x, end_y, board):
        pass

    #Return a list of possible capture coordinates
    #To be used to evaluate check/checkmate
    def possible_captures(self, board):
        moves = []
        pos = board.get_square(self)
        for i in range(8):
            for j in range(8):
                if (self.valid_capture(pos[0], pos[1], i, j)):
                    moves = moves.append(i, j)