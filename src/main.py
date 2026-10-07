import pygame
import sys  #helps us to quit the application

from const import * #gives us access to const.py constants 
from game import Game
from square import Square

class Main: 

    def __init__(self): #need to surround init with two underscores for it to work, default constructor
        pygame.init() #initializes our pygame model, always have to do this when working with pygame
        self.screen = pygame.display.set_mode( (WIDTH, HEIGHT) ) # creates a pygame screen 
        pygame.display.set_caption('Chess') 
        self.game = Game()

    def mainloop(self): 
       
       screen = self.screen
       game = self.game
       board = self.game.board
       dragger = self.game.dragger 

       while True: # infinite loop that keeps game running
           #show methods
           game.show_bg(screen) 
           game.show_moves(screen)
           game.show_pieces(screen) 

           if dragger.dragging: 
               dragger.update_blit(screen)

           for event in pygame.event.get(): #retrieves each event queued up since the last call, events include key presses, mouse clicks, etc.

               if event.type == pygame.MOUSEBUTTONDOWN: 
                   dragger.update_mouse(event.pos)

                   clicked_row = dragger.mouseY // SQSIZE
                   clicked_col = dragger.mouseX // SQSIZE

                   #if the clicked square has a piece?
                   if board.squares[clicked_row][clicked_col].has_piece(): 
                       piece = board.squares[clicked_row][clicked_col].piece 
                       board.calc_moves(piece, clicked_row, clicked_col)
                       dragger.save_initial(event.pos)
                       dragger.drag_piece(piece)

                       #show methods
                       game.show_bg(screen)
                       game.show_moves(screen)
                       game.show_pieces(screen)

               #mouse motion
               elif event.type == pygame.MOUSEMOTION: 
                   if dragger.dragging: 
                       dragger.update_mouse(event.pos)
                       #show methods
                       #game.show_bg(screen)
                       #game.show_moves(screen)
                       #game.show_pieces(screen)
                       #dragger.update_blit(screen)
                       

               #click release
               elif event.type == pygame.MOUSEBUTTONUP: 
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE
                        square = board.squares[released_row][released_col]
                    
                        if square.has_piece(): 
                            #Explosive capture of opponent pieces 
                            if square.piece.color != dragger.piece.color and (released_row, released_col) in [(move.final.row, move.final.col) for move in dragger.piece.moves]:
                                #Surrounding square locations that could be targets of the atomic explosion
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
                                potential_surrounding_targets = [board.squares[row][col] for (row, col) in potential_surrounding_targets]
                               
                                for target in potential_surrounding_targets: 
                                    if target.has_enemy_piece(dragger.piece.color) and not (target.piece.name == "pawn"):
                                        target.piece = None 
                                square.piece = None
                                board.squares[dragger.initial_row][dragger.initial_col].piece = None 
                                dragger.undrag_piece()
                            #if released over own team piece
                            elif square.piece.color == dragger.piece.color: 
                                dragger.undrag_piece()
                        #valid move?
                        elif (released_row, released_col) in [(move.final.row, move.final.col) for move in dragger.piece.moves]:
                            square.piece = dragger.piece
                            board.squares[dragger.initial_row][dragger.initial_col].piece = None 
                            dragger.undrag_piece()
                        else: 
                            dragger.undrag_piece()


                    #show methods
                    #game.show_bg(screen)
                    #game.show_moves(screen)
                    #game.show_pieces(screen)
                    #dragger.update_blit(screen)

               #quit application
               elif event.type == pygame.QUIT: #checks if the event is the user closing the pygame window (quitting the game)
                   pygame.quit()
                   sys.exit() #terminates the python program, stopping the ininite loop

           pygame.display.update() #updates our displayed screen
        
main = Main()
main.mainloop()