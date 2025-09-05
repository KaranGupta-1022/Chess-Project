from constants import SCREEN_WIDTH, SCREEN_HEIGHT, BOARD_ROW, BOARD_COL, SQUARE_SIZE
from square import Square
from piece import Pawn, King, Queen, Rook, Bishop, Knight
from move import Move

class Board:

    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(BOARD_COL)]
        self._create()
        self._add_pieces("white")
        self._add_pieces("black")
        self.last_move = None

    def _create(self):
        for row in range(BOARD_ROW):
            for col in range(BOARD_COL):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == "white" else (1, 0)
        # Creating Pawns
        for col in range(BOARD_COL):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))
        

        # Creating Knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # Creating Bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # Creating Rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # Creating King
        self.squares[row_other][4] = Square(row_other, 4, King(color))

        # Creating Queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

    def calc_moves(self, piece, row, col):
        
        def knight_moves():
            possible_moves = [(row-2, col-1), (row-1, col+2), (row+1, col+2), (row+2, col-1), (row+2, col+1), (row+1, col-2), (row-1, col-2), (row-2, col+1)]
            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].isempty_or_rivial(piece.color):
                        # Making a move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)
                        #Appending the move
                        piece.add_move(move)

        def pawn_moves():
            steps = 1 if piece.moved else 2
            # vertical move
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            for move_row in range(start, end, piece.dir):
                if Square.in_range(move_row):
                    if self.squares[move_row][col].isempty():
                        # Creating initial and final squares
                        initial = Square(row, col)
                        final = Square(move_row, col)
                        move = Move(initial, final)
                        piece.add_move(move)
                    else: 
                        break
                else:
                    break
            # diagonal move
            move_row = row + piece.dir
            move_cols = [col - 1, col + 1]
            for move_col in move_cols:
                if Square.in_range(move_row, move_col):
                    if self.squares[move_row][move_col].has_rivial_piece(piece.color):
                        # Creating initial and final squares
                        initial = Square(row, move_col)
                        final = Square(move_row, move_col)
                        move = Move(initial, final)
                        piece.add_move(move)

        def straight_move(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                while True:
                    if Square.in_range(possible_move_row, possible_move_col):

                        # Creating new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)

                        if self.squares[possible_move_row][possible_move_col].isempty():
                            # Add Move
                            piece.add_move(move)
                            
                        if self.squares[possible_move_row][possible_move_col].has_rivial_piece(piece.color):
                            # Add Move
                            piece.add_move(move)
                            break

                        if self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            # Add Move
                            break
                    
                    else:
                        break

                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr

        def king_moves():
            adjs = [(row-1, col+0), (row+1, col+0), (row+0, col-1), (row+0, col+1), (row-1, col-1), (row-1, col+1), (row+1, col-1), (row+1, col+1)]
            for adj in adjs:
                adj_row, adj_col = adj
                if Square.in_range(adj_row, adj_col):
                    if self.squares[adj_row][adj_col].isempty_or_rivial(piece.color):
                        initial = Square(row, col)
                        final = Square(adj_row, adj_col)
                        move = Move(initial, final)
                        piece.add_move(move)

        if isinstance(piece, Pawn):
            pawn_moves()
        elif isinstance(piece, Knight):
            knight_moves()
        elif isinstance(piece, Bishop):
            straight_move([(1, 1), (1, -1), (-1, 1), (-1, -1)])
        elif isinstance(piece, Rook):
            straight_move([(1, 0), (0, 1), (-1, 0), (0, -1)])
        elif isinstance(piece, Queen):
            straight_move([(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (0, 1), (-1, 0), (0, -1)])
        elif isinstance(piece, King):
            king_moves()

    def move(self, piece, move):
        initial = move.initial
        final = move.final

        # board update
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece
        # move
        piece.moved = True
        # check valid moves
        piece.clear_moves()
        self.last_move = move

    def valid_move(self, piece, move):
        return move in piece.moves