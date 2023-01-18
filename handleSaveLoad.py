import csv
from board import Board

class HandleCSV():
    
    filename = ""
    text_data = [
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
        [None, None, None, None, None, None, None, None],
    ]
    
    def __init__(self, filename):
        self.filename = filename

    def board_to_text(self, board):
        if isinstance(board, Board):
            for i in range(8):
                for j in range(8):
                    self.text_data[i].insert(j, board.get_piece_text(i, j))
                    self.text_data[i].pop(j + 1)

    #Takes Board object board
    def handle_save(self, board):
        with open(self.filename, 'w', newline='') as db:
            csvwriter = csv.writer(db, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            self.board_to_text(board)
            csvwriter.writerows(self.text_data)
            csvwriter.writerow([board.player])

    #Loads saved Board
    def handle_load(self, board):
        with open(self.filename, 'r', newline='') as db:
            csvreader = csv.reader(db, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            
            i = 0
            j = 0
            player = ""
            for row in csvreader:
                if i == 8:
                    player = row[0]
                    break
                for piece in row:
                    self.text_data[i].insert(j, piece)
                    self.text_data[i].pop(j + 1)
                    j +=1
                if j > 7:
                    j = 0
                i += 1
                

            if isinstance(board, Board):
                board.construct_board(self.text_data, player)
