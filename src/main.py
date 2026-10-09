import pygame
import sys  #helps us to quit the application

from const import * #gives us access to const.py constants 
from game import Game
from move import Move

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
           game.show_last_move(screen)
           game.show_moves(screen)
           game.show_pieces(screen) 

           if dragger.dragging: 
               dragger.update_blit(screen)
           game.show_game_over(screen)

           for event in pygame.event.get(): #retrieves each event queued up since the last call, events include key presses, mouse clicks, etc.

               if event.type == pygame.MOUSEBUTTONDOWN: 
                   dragger.update_mouse(event.pos)

                   clicked_row = dragger.mouseY // SQSIZE
                   clicked_col = dragger.mouseX // SQSIZE

                   #if the clicked final_square has a piece?
                   if game.winner is None and board.squares[clicked_row][clicked_col].has_piece(): 
                       piece = board.squares[clicked_row][clicked_col].piece 
                       #if it is this player's turn
                       if piece.color == game.next_player:
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
                        initial_square = board.squares[dragger.initial_row][dragger.initial_col]
                        final_square = board.squares[released_row][released_col]

                        #Valid move?
                        if (released_row, released_col) in [(move.final.row, move.final.col) for move in dragger.piece.moves]: 
                            captured = final_square.has_piece()
                            board.move(dragger.piece, Move(initial_square, final_square))
                            game.play_sound(captured)
                            dragger.undrag_piece()
                            #track last move for highlight
                            board.last_move = Move(initial_square, final_square)
                            game.next_turn()
                            game.check_game_over()
                        else: 
                            dragger.undrag_piece()
                        
                        game.show_last_move(screen)

               #quit application
               elif event.type == pygame.QUIT: #checks if the event is the user closing the pygame window (quitting the game)
                   pygame.quit()
                   sys.exit() #terminates the python program, stopping the ininite loop

           pygame.display.update() #updates our displayed screen
        
main = Main()
main.mainloop()