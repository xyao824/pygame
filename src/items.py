import pygame
from random import randrange, uniform

IMAGE_PATH = '../image/'

class Item(pygame.sprite.Sprite):
    def __init__(self, image, x, y, item_type):
        super(Item, self).__init__()
        self.speed = 5
        self.live = True
        self.image = pygame.image.load(f'{IMAGE_PATH}/{image}')
        self.item_type = item_type
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if randrange(1, 3) % 2:
            self.x_speed = self.speed
            print(self.x_speed)
        else:
            self.x_speed = - self.speed
            print(self.x_speed)
    def display_item(self, screen):
        screen.blit(self.image,self.rect)
    

    def item_move(self, screen):
        w, h = screen.get_size()
        # Bounce off the screen boundaries
        if self.rect.x <= 0 and self.rect.y <= 900:
            self.rect.x += abs(self.x_speed)
            self.rect.y += self.speed
            self.x_speed = -self.x_speed
        elif self.rect.x >= w-36 and self.rect.y <= 900:
            self.rect.x -= abs(self.x_speed)
            self.rect.y += self.speed
            if self.rect.x <= w:
                self.x_speed = -self.x_speed
        elif self.rect.y > 900:
            self.live = False
        else:
            self.rect.x -= self.x_speed
            self.rect.y += self.speed
