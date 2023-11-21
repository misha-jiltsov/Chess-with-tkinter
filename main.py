

import tkinter as tk
from tkinter import messagebox




class Board:
    def __init__(self, master, pieces):
        self.master = master
        self.master.title = "Chess"
        self.white_turn = True
        self.main_frame = tk.Frame(master)
        self.board_display = [[tk.Button(master, bg="grey") if i%2==0 else tk.Button(master, bg="white") for i in range(8)] if i%2!=0 else [tk.Button(master, bg="white") if i%2==0 else tk.Button(master, bg="grey") for i in range(8)] for i in range(8)]
        for i, row in enumerate(self.board_display):
            for j, button in enumerate(row):
                coords = [j, i]
                button.config(command=lambda coord = coords: self.piece_action(coord))

        self.pieces = pieces
        self.selected_piece = None
        self.board = [[None for i in range(8)] for i in range(8)]
        self.king_in_check = [False, False]
        self.default_boardpos = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR"
        self.board_rows_setup = self.default_boardpos.split("/")
        self.piece_notations = {
            "r": Rook("black", self.board),
            "n": Knight("black", self.board),
            "b": Bishop("black", self.board),
            "q": Queen("black", self.board),
            "k": King("black", self.board),
            "p": Pawn_Black("black", self.board),
            "R": Rook("white", self.board),
            "N": Knight("white", self.board),
            "B": Bishop("white", self.board),
            "Q": Queen("white", self.board),
            "K": King("white", self.board),
            "P": Pawn_White("white", self.board)
        }


        self.selected_label = tk.Label(master, text = f"selected: {self.selected_piece}")
        self.selected_label.grid(column = 10, row  = 0)


        for i, row in enumerate(self.board_display):
            for j, sqr  in enumerate(row):
                sqr["width"], sqr["height"] = 5,2
                sqr.grid(column = j, row = i)

        self.setup_board()
        print(self.board)





    def setup_board(self):
        ################### DISPLAY BOARD

        character_setup = []
        for i, item in enumerate(self.board_rows_setup):
            row = []
            for j, elem in enumerate(item):
                if not elem.isdigit():
                    row.append(elem)

                    self.board[i][j] = self.piece_notations[elem]
                    self.pieces.append(self.board[i][j])

                elif elem.isdigit():
                    for i in range(int(elem)):
                        row.append("")


            character_setup.append(row)
            print(row)

        for i, row in enumerate(self.board_display):
            for j, elem in enumerate(row):
                elem["text"] = character_setup[i][j]
                elem.update()





        ########################## CLASS BOARD

        # for i, row in enumerate(self.board_display):
        #     for j, elem in enumerate(row):
        #         if elem!="":
        #





    def update_pieces(self):

        for i, row in enumerate(self.board):
            for j, tile in enumerate(row):
                if j!=None:
                    self.board_display[i][j]




    def change_turn(self):
        if self.white_turn:
            self.white_turn = False
        else:
            self.white_turn = True



    def piece_action(self, coords):
        target = self.board[coords[1]][coords[0]]
        if self.selected_piece==None and target!=None:
            if (target.show_colour() == "white" and self.white_turn) or (target.show_colour == "black" and not self.white_turn):
                self.selected_piece = target
                self.selected_label["text"] = f"selected: {self.selected_piece}"
                self.selected_label.update()
        elif self.selected_piece!=None and target == None:
            pass




class Piece:
    def __init__(self, colour, board):
        self.colour = colour
        self.movepatterns = ["0 0 1"]
        self.board = board
        self.moved = False
        self.type = "default_piece"
        self.position = [None, None]

        if self.colour=="black":
            self.display_item = "r"
        elif self.colour == "white":
            self.display_item = "R"

    def return_disp_char(self):
        return self.display_item

    def set_pos(self, pos):
        self.position = pos

    def move(self, pos):
        if pos in self.determine_all_moves(self.position):
            self.position = pos
            return pos

    def show_colour(self):
        return self.colour
    def determine_all_moves(self, position):
        cur_pos = [position[0], position[1]]
        coords = []

        for pat in self.movepatterns:
            split = pat.split(" ")
            change_x, change_y, repetitions = int(split[0]), int(split[1]), int(split[2])

            for i in range(repetitions):
                coords_new = [cur_pos[0]+(change_x*(i+1)), cur_pos[1]+(change_y*(i+1))]
                if self.determine_valid_move(coords_new):
                    coords.append(coords_new)


        return coords

    def determine_valid_move(self, move_coords):
        if True not in self.board.king_in_check:
            if self.board[move_coords[0]][move_coords[1]] != None:
                return False
            elif move_coords[0]<0 or move_coords[1]<0:
                return False
            else:
                return True
        else:
            return


class Pawn_Black (Piece):
    def __init__(self, colour, board):
        super().__init__(colour, board)
        self.colour = colour
        self.movepatterns = ["0 -1 1"]
        self.display_item = "p"
        self.type = "pawn"






    def determine_valid_move(self, move_coords):
        if self.board[move_coords[0]][move_coords[1]] != None:
            return False
        elif move_coords[0]<0 or move_coords[1]<0:
            return False
        elif self.moved == True and abs(move_coords[1]-self.position[1])==2:
            return False
        else:
            return True


class Pawn_White (Piece):
    def __init__(self, colour, board):
        super().__init__(colour, board)
        self.display_item = "P"
        self.movepatterns = ["0 1 1"]
        self.type = "pawn"

    def determine_valid_move(self, move_coords):

        if self.board[move_coords[0]][move_coords[1]] != None:
            return False
        elif move_coords[0]<0 or move_coords[1]<0:
            return False
        elif self.moved == True and abs(move_coords[1]-self.position[1])==2:
            return False
        else:
            return True

class Rook (Piece):
    def __init__(self, colour, board):
        super().__init__(colour, board)
        self.movepatterns = ["1 0 8", "0 1 8", "-1 0 8", "0 -1 8"]
        self.type = "rook"


class Knight (Piece):
    def __init__(self, colour, board):
        super().__init__(colour, board)
        self.movepatterns = ["1 2 1", "-1 2 1", "2 1 1", "2 -1 1", "-2 1 1", "-2 -1 1", "-1 -2 1", "1 -2 1"]
        self.type = "knight"

class Bishop (Piece):
    def __init__(self, colour, board):
        super().__init__(colour, board)
        self.movepatterns = ["1 1 8", "1 -1 8", "-1 1 8", "-1 -1 8"]
        self.type = "bishop"

class King (Piece):
    def __init__(self, colour, board):
        super().__init__(colour, board)
        self.movepatterns = ["1 1 1", "1 -1 1", "-1 1 1", "-1 -1 1"]
        self.type = "king"

class Queen (Piece):
    def __init__(self, colour, board):
        super().__init__(colour, board)
        self.movepatterns = ["1 1 8", "1 -1 8", "-1 1 8", "-1 -1 8", "1 0 8", "0 1 8", "-1 0 8", "0 -1 8"]
        self.type = "queen"






if __name__ == "__main__":
    root = tk.Tk()
    game = Board(root, [])
    root.mainloop()
