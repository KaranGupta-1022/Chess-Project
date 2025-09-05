import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, BOARD_ROW, BOARD_COL, SQUARE_SIZE
from board import Board
from dragger import Dragger

class Game:

    def __init__(self):
        self.board = Board()
        self.dragger = Dragger()
        self.next_player = "white"
        self.hovered_sqr = None

    def show_background(self, surface):
        for row in range(BOARD_ROW):
            for col in range(BOARD_COL):
                if (row + col) % 2 == 0:
                    # light green 
                    color = (255, 255, 255)
                else: 
                    # dark green
                    color = (119, 154, 88)

                rect = pygame.Rect(col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(surface, color, rect)

    def show_pieces(self, surface):
        for row in range(BOARD_ROW):
            for col in range(BOARD_COL):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    # Assuming piece has a texture attribute for the image path
                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80)
                        img = pygame.image.load(piece.texture)
                        img_center = col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)
    
    def show_moves(self, surface):
        if self.dragger.dragging:
            piece = self.dragger.piece
            for move in piece.moves:
                color = '#C86464'if (move.final.row + move.final.col) % 2 == 0 else '#684646'
                rect = pygame.Rect(move.final.col * SQUARE_SIZE, move.final.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(surface, color, rect)  
    
    def next_turn(self):
        self.next_player = "white" if self.next_player == "black" else "black"

    def show_last_move(self, surface):
        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final
            for pos in [initial, final]:
                color = (244, 247, 116) if (pos.row + pos.col) % 2 == 0 else (172, 195, 51)
                rect = pygame.Rect(pos.col * SQUARE_SIZE, pos.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(surface, color, rect)  

    def show_hover(self, surface):
        if self.hovered_sqr:
            color = (180, 180, 180)
            rect = pygame.Rect(self.hovered_sqr.col * SQUARE_SIZE, self.hovered_sqr.row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
            pygame.draw.rect(surface, color, rect, width=3)

    def set_hover(self, row, col):
        self.hovered_sqr = self.board.squares[row][col]