import pygame
class Tiles():
    def __init__(self, x, y, width, height, img, id) -> None:
        self.rect = pygame.rect.Rect(x,y,width,height)
        self.img = img
        self.id = id
        self.display_x = 0
        self.display_y = 0
    
    def draw(self, display, scroll):
        self.display_x = self.rect.x
        self.display_y = self.rect.y
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]
        display.blit(self.img, self.rect)
        self.rect.x = self.display_x
        self.rect.y = self.display_y
    
    def get_rect(self):
        return self.rect

    def get_id(self):
        return self.id