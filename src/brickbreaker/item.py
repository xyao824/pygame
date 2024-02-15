import pygame
import os
from random import randrange, uniform


IMAGE_PATH = 'image/'
# Mapping for items
ITEMS_LIST = {
    "item_A.png": "timesthree", # +3 balls at ball position 
    "item_B.png": "shotthree",
    "item_C.png": "expandbar"   # +3 balls at the bar postition
}

class Item (pygame.sprite.Sprite):
    def __init__(self, index, center, screen, item_speed):
        self.speed = item_speed
        self.live = True
        self.screen = screen
        self.load_image(list(ITEMS_LIST.keys())[index])
        self.item_type = list(ITEMS_LIST.values())[index]
        self.rect.x = center[0]
        self.rect.y = center[1]

    def load_image(self, filename):
        self.image = pygame.image.load(os.path.join(os.getcwd(), IMAGE_PATH, filename))
        self.rect = self.image.get_rect()
    
    def display_item(self):
        self.screen.blit(self.image, self.rect)

    def item_fall(self):
        w, h = self.screen.get_size()
        if self.live:
            if self.rect.bottom < h:
                self.rect.y += self.speed
            else:
                self.live = False
        else:
            pass
