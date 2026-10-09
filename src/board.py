from const import * 
from square import * 
from piece import * 
from move import Move
import copy

class Board: 

    def __init__(self): 
        self.squares = [[0 for zero in range(ROWS)] for col in range(COLS)]
        self.last_move = None
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def in_check(self, piece, move):
        temp_piece = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_piece, move)

        mine = False
        enemy = False
        for row in temp_board.squares:
            for square in row:
                if isinstance(square.piece, King):
                    if square.piece.color == piece.color:
                        mine = True
                    else:
                        enemy = True

        if not mine: return True    
        if not enemy: return False  
        return temp_board.king_attacked(piece.color)

    def king_attacked(self, color):
        for row in range(ROWS):
            for col in range(COLS):
                if self.squares[row][col].has_enemy_piece(color):
                    p = self.squares[row][col].piece
                    self.calc_moves(p, row, col, bool=False)
                    for m in p.moves:
                        target = self.squares[m.final.row][m.final.col].piece
                        if isinstance(target, King) and target.color == color:
                            return True
        return False

    def has_legal_moves(self, color):
        for row in range(ROWS):
            for col in range(COLS):
                if self.squares[row][col].has_team_piece(color):
                    p = self.squares[row][col].piece
                    self.calc_moves(p, row, col)
                    if p.moves:
                        return True
        return False

    def move(self, piece, move):
        initial = move.initial
        final = move.final
        captured = self.squares[final.row][final.col].has_piece()

        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        piece.moved = True
        piece.moves = []

        if captured:
            # explosive capture of surrounding pieces that are not pawns
            for target in self.calc_atomic_targets(self.squares[final.row][final.col]):
                if target.has_enemy_piece(piece.color) and target.piece.name != "pawn":
                    target.piece = None
            self.squares[final.row][final.col].piece = None  #capturing piece explodes too
        return captured

    #Calculates all the possible (valid) moves of a specific piece on a specific position
    def calc_moves(self, piece, row, col, bool=True):
        piece.moves = [] #start from a fresh list so previous moves not initially possible 
            

        def pawn_moves(): 
            #steps -> 1 if pawn has not moved yet
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

                        #check potential checks, bool avoids infinite loop
                        if bool: 
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else: 
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
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)
                        if bool: 
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else: 
                            piece.add_move(move)
                        
                       

            
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
                        final_piece = self.squares[possible_row][possible_col].piece
                        final = Square(possible_row, possible_col) #piece = piece
                        move = Move(initial, final)

                        if bool: 
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)

        def straightline_moves(incrs): 
            for incr in incrs: 
                row_incr, col_incr = incr
                possible_move_row = row + row_incr 
                possible_move_col = col + col_incr 

                while True:
                    if Square.in_range(possible_move_row,possible_move_col): 
                        #create squares of possible new move
                        initial = Square(row,col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col)
                        #create a possible new move 
                        move = Move(initial, final)

                        # empty -> continue looping
                        if self.squares[possible_move_row][possible_move_col].is_empty(): 
                            if bool: 
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else: 
                                piece.add_move(move)

                        #has enemy piece
                        elif self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color): 
                            #append new move
                            if bool: 
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else: 
                                piece.add_move(move)
                            break

                        #has team piece = break
                        elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color): 
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
            for possible_move in adjacents: 
                possible_row, possible_col = possible_move
                if Square.in_range(possible_row, possible_col): 
                    if self.squares[possible_row][possible_col].isempty_or_enemy(piece.color): 
                        #create squares of new move
                        initial = Square(row, col)
                        final = Square(possible_row, possible_col) #piece = piece
                        move = Move(initial, final)
                        if bool: 
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else: 
                            piece.add_move(move)
            
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

    def calc_atomic_targets(self, square):
        potential_surrounding_targets = [ 
            (square.row +1, square.col), #down
            (square.row -1, square.col), #up
            (square.row, square.col -1), #left
            (square.row, square.col +1), #right
            (square.row +1, square.col+1), #down-right
            (square.row +1, square.col-1), #down-left
            (square.row -1, square.col-1), #up-left
            (square.row -1, square.col+1), #up-right
        ]
                
        potential_surrounding_targets = [t for t in potential_surrounding_targets if Square.in_range(*t)] #filters out spaces out-of-range 
        return [self.squares[row][col] for (row, col) in potential_surrounding_targets] 


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
        self.squares[row_other][4] = Square(row_other, 4, King(color))

b = Board()
b._create()