from const import * 
from square import * 
from piece import * 
from move import Move

class Board: 

    def __init__(self): 
        self.squares = [[0 for zero in range(ROWS)] for col in range(COLS)]

        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    #Calculates all the possible (valid) moves of a specific piece on a specific position
    def calc_moves(self, piece, row, col): 

        def pawn_moves(): 
            #steps 
            steps = 1 if piece.moved else 2

            #vertical moves
            start = row + piece.dir #lower end of vertical move range, one space away
            end = row + (piece.dir * (1 + steps)) #end of vertical move range, exclusive in range function
            for possible_move_row in range(start, end, piece.dir): 
                if Square.in_range(possible_move_row): 
                    if self.squares[possible_move_row][col].is_empty(): 
                        #create initial and final move squares
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)
                        #create a new move
                        move = Move(initial, final)
                        piece.add_move(move)
                    #vertical movement blocked
                    else: break
                #vertical moves not in range
                else: break

            #diagonal moves
            possible_move_row = row + piece.dir
            possible_move_cols = [col-1, col+1]
            for possible_move_col in possible_move_cols: 
                if Square.in_range(possible_move_row, possible_move_col): 
                    if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        piece.add_move(Move(initial, final))

            
        def knight_moves(): 
            #8 possible moves
            possible_moves = [
                (row-2, col+1), 
                (row-1, col+2),
                (row+1, col+2),
                (row+2, col+1),
                (row+2, col-1),
                (row+1, col-2),
                (row-1, col-2),
                (row-2, col-1),
            ]

            for possible_move in possible_moves: 
                possible_row, possible_col = possible_move
                if Square.in_range(possible_row, possible_col): 
                    if self.squares[possible_row][possible_col].isempty_or_enemy(piece.color): 
                        #create squares of new move
                        initial = Square(row, col)
                        final = Square(possible_row, possible_col) #piece = piece
                        piece.add_move(Move(initial, final))


        if isinstance(piece, Pawn): pawn_moves()

        if isinstance(piece, Knight): knight_moves()
        
        if isinstance(piece, Bishop): pass

        if isinstance(piece, Rook): pass

        if isinstance(piece, Queen): pass


    def _create(self): #uses an _ before to indicate this is a private function uses only within Board class
        self.squares = [[Square(row, col) for col in range(COLS)] for row in range(ROWS)]
       

    def _add_pieces(self, color):
        row_pawn, row_other = (ROWS-2, ROWS -1) if color == 'white' else (1, 0)

        # pawns
        for col in range(COLS): 
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        #knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))
        self.squares[4][4] = Square(4, 4, Knight(color))

        #bishops 
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        #rook
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        #queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        #king
        self.squares[row_other][4] = Square(row_other, 3, King(color))

b = Board()
b._create()