class Piece:
    row = 0
    col = 0
    color = None
    possible_moves = []

    def __init__(self, color):
        self.color = color
    
    def draw(self):
        pass

    #Checks if a given move is valid
    def valid_move(self, start_x, start_y, end_x, end_y, board):
        pass

    #Checks if a given capture is valid (ie, account for pawn's different capture behavior)
    def valid_capture(self, start_x, start_y, end_x, end_y, board):
        pass

    