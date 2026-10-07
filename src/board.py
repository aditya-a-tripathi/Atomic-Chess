from const import * 
from square import * 
from piece import * 
from move import Move

class Board: 

    def __init__(self): 
        self.squares = [[0 for zero in range(ROWS)] for col in range(COLS)]
        self.last_move = None
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')


    #Calculates all the possible (valid) moves of a specific piece on a specific position
    def calc_moves(self, piece, row, col):
        piece.moves = [] #start from a fresh list so previous moves not initially possible 

        def add_knight_or_king_moves(possible_moves): 
            for possible_move in possible_moves: 
                possible_row, possible_col = possible_move
                if Square.in_range(possible_row, possible_col): 
                    if self.squares[possible_row][possible_col].isempty_or_enemy(piece.color): 
                        #create squares of new move
                        initial = Square(row, col)
                        final = Square(possible_row, possible_col) #piece = piece
                        piece.add_move(Move(initial, final))

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

            add_knight_or_king_moves(possible_moves)

        def straightline_moves(incrs): 
            for incr in incrs: 
                row_incr, col_incr = incr
                possible_move_row = row + row_incr 
                possible_move_col = col + col_incr 

                while True:
                    if Square.in_range(possible_move_row,possible_move_col): 
                        #create squares of possible new move
                        initial = Square(row,col)
                        final = Square(possible_move_row, possible_move_col)
                        #create a possible new move 
                        move = Move(initial, final)

                        # empty -> continue looping
                        if self.squares[possible_move_row][possible_move_col].is_empty(): 
                            #append new move
                            piece.add_move(move)

                        #has enemy piece
                        if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color): 
                            #append new move
                            piece.add_move(move)
                            break

                        #has team piece = break
                        if self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color): 
                            break
                    
                    #not in range
                    else: 
                        break 
                    #Incrementing incrs  
                    possible_move_row = possible_move_row + row_incr 
                    possible_move_col = possible_move_col + col_incr

        def king_moves(): 
            pass
            adjacents = [
                (row -1, col), # up 
                (row -1 , col +1), # up-right
                (row, col + 1), # right
                (row + 1 , col), # down
                (row + 1, col + 1), # down-right
                (row + 1 , col -1), # down-left
                (row, col -1), # left
                (row - 1, col -1), # up-left
            ]
            #Normal moves
            add_knight_or_king_moves(adjacents)
            
        if isinstance(piece, Pawn): pawn_moves()

        elif isinstance(piece, Knight): knight_moves()
        
        elif isinstance(piece, Bishop): 
            straightline_moves([
                (-1, 1), # Up right
                (-1, -1), # Up left
                (1, 1), # down right 
                (1, -1) #down left 
            ])

        elif isinstance(piece, Rook): 
            straightline_moves([ 
                (-1, 0), #up 
                (0, 1), #right
                (1, 0),  #down
                (0, -1) #left
            ])

        elif isinstance(piece, Queen): 
            straightline_moves([
                (-1, 1), # Up right
                (-1, -1), # Up left
                (1, 1), # down right 
                (1, -1), #down left 
                (-1, 0), #up 
                (0, 1), #right
                (1, 0),  #down
                (0, -1) #left
            ])

        elif isinstance(piece, King): king_moves()


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