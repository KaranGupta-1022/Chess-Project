import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, BOARD_ROW, BOARD_COL, SQUARE_SIZE

class Dragger:

    def __init__(self):
        self.mouseX = 0
        self.mouseY = 0
        self.initialRow = 0
        self.initialCol = 0
        self.piece = None
        self.dragging = False

    def update_mouse(self, pos):
        self.mouseX, self.mouseY = pos

    def save_inital(self, pos):
        self.initialRow = pos[1] // SQUARE_SIZE
        self.initialCol = pos[0] // SQUARE_SIZE 

    def drag_piece(self, piece):
        self.piece = piece
        self.dragging = True

    def release_piece(self):
        self.piece = None
        self.dragging = False

    def update_blit(self, surface):
        #Texture
        self.piece.set_texture(size = 128)
        texture = self.piece.texture
        #Image
        img =  pygame.image.load(texture)
        #Rectangele
        img_center = (self.mouseX, self.mouseY)
        self.piece.texture_rect = img.get_rect(center=img_center)
        #Update Blit
        surface.blit(img, self.piece.texture_rect)