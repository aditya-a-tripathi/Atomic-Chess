import os 

class Piece: 

    def __init__(self, name, color, value, texture = None, texture_rect = None):
        self.name = name 
        self.color = color
        value_sign = 1 if color == 'white' else -1  
        self.value = value * value_sign #value conveys to the AI how important a piece is 
        self.moves = []
        self.moved = False
        self.texture = texture
        self.set_texture()
        self.texture_rect = texture_rect 

    def set_texture(self, size = 80): #texture is a path/url to the specific asset image
        self.texture = os.path.join(
            f'assets/images/imgs-{size}px/{self.color}_{self.name}.png' #accessing the asset at the specific file path
        )

    def add_move(self, move): 
        self.moves.append(move)


class Pawn(Piece): #tells python Pawn inherits from the Piece class
    def __init__(self, color): #taking the color because that tells us the direction the pawn should move
        self.dir = -1 if color == "white" else 1 #pygame has x increasing left to right and y increasing downwards so -1 means moving up
        super().__init__('pawn', color, 1.0) 

class Knight(Piece): 

    def __init__(self, color): 
        super().__init__("knight", color, 3.001)

class Bishop(Piece): 
    
    def __init__(self, color): 
        super().__init__("bishop", color, 3.0)

class Rook(Piece): 
    
    def __init__(self, color): 
        super().__init__("rook", color, 5.0)

class Queen(Piece): 
    
    def __init__(self, color): 
        super().__init__("queen", color, 9.0)

class King(Piece): 
    
    def __init__(self, color): 
        super().__init__("king", color, 10000)

    

    