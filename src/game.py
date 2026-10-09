import pygame 

from const import * 
from board import Board
from dragger import Dragger 
from config import Config
from piece import King

class Game: 

    def __init__(self): 
        self.next_player = "white"
        self.winner = None
        self.board = Board()
        self.dragger = Dragger() 
        self.config = Config()

    #Show methods 

    def show_bg(self, surface): 

        for row in range(ROWS): 
            for col in range(COLS): 
                if (row + col) % 2 == 0: #for checkered pattern, even numbers are every other number in the loop
                    color = (234, 235, 200)
                else: 
                    color = (119, 154, 88) 

                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE) #creates the squares (x pos, y pos, width, height)

                pygame.draw.rect(surface, color, rect)

    def show_pieces(self, surface): 
        for row in range(ROWS): 
            for col in range(COLS): 
                if self.board.squares[row][col].has_piece(): 
                    piece = self.board.squares[row][col].piece 

                    #all pieces except dragger piece
                    if self.dragger.piece is not piece: 
                        img = pygame.image.load(piece.texture) #stores the image asset found at that texture path
                        img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                        piece.texture_rect = img.get_rect(center = img_center)
                        surface.blit(img, piece.texture_rect) #draws the image pixels onto the surface at that position

    def show_moves(self, surface): 
        if self.dragger.dragging: 
            piece = self.dragger.piece

            #loop all valid moves
            for move in piece.moves: 
                #color
                color = '#C86464' if (move.final.row + move.final.col) % 2 == 0 else '#C86464'
                #rect
                rect = (move.final.col * SQSIZE, move.final.row * SQSIZE, SQSIZE, SQSIZE)
                #blit
                pygame.draw.rect(surface, color, rect)
        
    def show_last_move(self, surface): 
        if self.board.last_move: 
            initial = self.board.last_move.initial
            final = self.board.last_move.final

            for pos in [initial,final]: 
                #color
                color = (244, 247, 116) if (pos.row + pos.col) % 2 == 0 else (172, 195, 51)
                #rect
                rect = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)
                #blit
                pygame.draw.rect(surface, color, rect)
               
    #other methods 

    def next_turn(self): 
        self.next_player = 'white' if self.next_player == "black" else "black"

    def check_game_over(self):
        color = self.next_player                    
        other = 'white' if color == 'black' else 'black'

        kings = [square.piece.color for row in self.board.squares for square in row if isinstance(square.piece, King)]
         # this player's king was blown up so other king wins
        if color not in kings:
            self.winner = other  

        elif not self.board.has_legal_moves(color):
            if self.board.king_attacked(color):
                #checkmate
                self.winner = other                 
            else:
                # stalemate
                self.winner = 'draw'                

    def show_game_over(self, surface):
        if self.winner is None: return
        font = pygame.font.SysFont('arial', 60, bold=True)
        text = 'Draw (stalemate)' if self.winner == 'draw' else f'{self.winner.capitalize()} wins!' 
        label = font.render(text, True, (255, 255, 255))
        rect = label.get_rect(center = (WIDTH // 2, HEIGHT // 2))
        pygame.draw.rect(surface, (78, 120, 55), rect.inflate(60, 40))
        surface.blit(label, rect)

    def play_sound(self, captured=False): 
        if captured: 
            self.config.capture_sound.play()
        else: 
            self.config.move_sound.play()
