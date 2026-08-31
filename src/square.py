from const import * 

class Square: 
    def __init__(self, row, col, piece=None): #parameter constructor, piece has default value of None
        self.row = row
        self.col = col 
        self.piece = piece

    def has_piece(self): 
        return self.piece != None

    def is_empty(self):
        return not self.has_piece()

    def has_team_piece(self, color): 
        return self.has_piece and self.piece.color == color
    
    def has_enemy_piece(self, color): 
        return self.has_piece() and self.piece.color != color

    def isempty_or_enemy(self, color): 
        return not self.has_piece() or self.has_enemy_piece(color)

    @staticmethod #this method applies to all intances of a class, can be called on the class itself rather than a specific instance
    def in_range(*args): 
        for arg in args: 
            if arg < 0 or arg > 7: 
                return False
            
        return True

