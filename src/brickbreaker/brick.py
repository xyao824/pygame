import pygame
import os
import math
from random import randrange, uniform
from item import Item
IMAGE_PATH = 'image/'

class Block(pygame.sprite.Sprite):
    def __init__(self, screen):
        super().__init__()
        self.live = True
        self.screen = screen

    def display_block(self):
        """
        Draw Block on the screen
        """
        self.screen.blit(self.image, self.rect)

    def load_image(self, filename):
        self.image = pygame.image.load(os.path.join(os.getcwd(), IMAGE_PATH, filename))
        self.rect = self.image.get_rect()
    
    def generate_item(self, center, items_lt):
        if randrange(1, 11) in [1, 2]:
            index = randrange(0, 3)
            item = Item(index, center, self.screen, item_speed=5)
            items_lt.append(item)
        
        return items_lt

    def hit_ball(self, ball, items_lt):
        
        # Calculate the distance between the centers of the ball and the block
        distance = math.sqrt((ball.center[0] - self.rect.centerx)**2 + (ball.center[1] - self.rect.centery)**2)

        # Check if there is a collision
        if distance < ball.radius + self.rect.width / 2:
            self.live = False
            if self.type == "Brick":
                items_lt = self.generate_item(ball.center, items_lt)
            # Check the side of the collision
            if ball.center[0] > self.rect.left and ball.x_speed > 0:                   
                # print("Hit left")
                ball.x_speed = -ball.x_speed
            elif ball.center[0] < self.rect.right and ball.x_speed < 0:
                # print("Hit right")
                ball.x_speed = -ball.x_speed
            elif ball.center[1] > self.rect.top and ball.y_speed > 0:
                # print("Hit top")
                ball.y_speed = -ball.y_speed
            elif ball.center[1] < self.rect.bottom and ball.y_speed < 0:
                # print("Hit bottom")
                ball.y_speed = -ball.y_speed
            else:
                ball.y_speed = -ball.y_speed
                ball.x_speed = -ball.x_speed

        return items_lt


class Brick(Block):
    def __init__(self, x, y, screen):
        super().__init__(screen)
        self.load_image('brick.png')
        self.rect.x = x
        self.rect.y = y
        self.type = 'Brick'

class Wall(Block):
    def __init__(self, x, y, screen):
        super().__init__(screen)
        self.load_image('wall.png')
        self.rect.x = x
        self.rect.y = y
        self.type = 'Wall'