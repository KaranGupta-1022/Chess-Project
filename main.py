import pygame
import sys

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, BOARD_ROW, BOARD_COL, SQUARE_SIZE
from game import Game
from dragger import Dragger
from square import Square   
from move import Move

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Chess Game")
        self.game = Game()
        self.dragger = Dragger()

    def mainloop(self):
        game = self.game
        screen = self.screen
        board = self.game.board
        dragger = self.game.dragger

        while True:
            game.show_background(screen)
            game.show_last_move(screen) 
            game.show_moves(screen)
            game.show_pieces(screen)
            game.show_hover(screen)

            if dragger.dragging:
                dragger.update_blit(screen)

            for event in pygame.event.get():
                # Handle events
                # Clicking Pieces
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)
                    clicked_row = dragger.mouseY // SQUARE_SIZE
                    clicked_col = dragger.mouseX // SQUARE_SIZE

                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        #valid player
                        if piece.color == game.next_player: 
                            board.calc_moves(piece, clicked_row, clicked_col)
                            dragger.save_inital(event.pos)
                            dragger.drag_piece(piece)
                
                            # Showing the moves
                            game.show_background(screen)
                            game.show_last_move(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)

                # Moving the Piece
                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQUARE_SIZE
                    motion_col = event.pos[0] // SQUARE_SIZE
                    game.set_hover(motion_row, motion_col)

                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        game.show_background(screen)
                        game.show_last_move(screen)
                        game.show_moves(screen)
                        game.show_pieces(screen)
                        game.show_hover(screen)
                        dragger.update_blit(screen)

                # Releasing the Piece
                elif event.type == pygame.MOUSEBUTTONUP:
                    
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        released_row = dragger.mouseY // SQUARE_SIZE
                        released_col = dragger.mouseX // SQUARE_SIZE

                        initial= Square(dragger.initialRow, dragger.initialCol)
                        final = Square(released_row, released_col)  
                        move = Move(initial, final)

                        # checking if valid move
                        if board.valid_move(dragger.piece, move):
                            board.move(dragger.piece, move)
                            # draw
                            game.show_background(screen)
                            game.show_last_move(screen) 
                            game.show_pieces(screen)
                            # next player
                            game.next_turn()

                    dragger.release_piece()


                # Leaving the Game
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update() 
                    

main = Main()
main.mainloop()
