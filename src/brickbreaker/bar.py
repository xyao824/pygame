import os
import pygame
from ball import Ball

IMAGE_PATH = 'image/'

class Bar(pygame.sprite.Sprite):

    def __init__(self, x, y, screen, bar_image):
        self.load_image(bar_image)
        self.rect.x = x
        self.rect.y = y
        self.speed = 10
        self.screen = screen

    def load_image(self, filename):
        """
        load the image from the filename
        """
        self.image = pygame.image.load(f'{os.getcwd()}/{IMAGE_PATH}/{filename}')
        self.rect = self.image.get_rect()

    def display_bar(self):
        """
        draw bar on screen
        """
        self.screen.blit(self.image, self.rect)
        

    def move_bar(self, post_x):
        """
        if bar.x is not equal to post_x and post_x is on the left of the bar
        then bar move to left

        else if bar.x is not equal to post_x and post_x is on the right of the bar
        then bar move to right
        """
        if self.rect.x <= post_x <= self.rect.x+96:
            pass
        else:
            if post_x > self.rect.x+96:
                self.rect.x += self.speed
            elif post_x < self.rect.x:
                self.rect.x -= self.speed
            else:
                pass
    
    def hit_ball(self, ball):
        """
        if the bar hit the ball, rebound the ball
        """
        hitted = False

        if self.rect.topleft[0]<= ball.center[0] <=self.rect.topright[0] and\
            self.rect.topleft[1] <= ball.center[1]+ball.radius and\
            ball.y_speed > 0:
            hitted = True
            ball.y_speed = -ball.y_speed
        return hitted
    
    def hit_item(self, item, ball, balls_lt):
        wider_bar = self
        if pygame.sprite.collide_rect(self, item):
            item.live = False
            if item.item_type == "timesthree":
                # print("timesthree")
                balls_lt = ball.times_threeballs(balls_lt)
            elif item.item_type == "shotthree":
                # print("shotthree")
                balls_lt = self.shot_threeballs(balls_lt)
            elif item.item_type == "expandbar":
                wider_bar = Bar(self.rect.topleft[0]-24, self.rect.top, self.screen, "wider_bar.png")
        return balls_lt, wider_bar
    
    def shot_threeballs(self, balls_lt):
        """
        shot three balls at the center of the bar position
        """
        center = (self.rect.topleft[0] + (self.rect.topright[0] - self.rect.topleft[0])/2, self.rect.topleft[1])
        w, h = self.screen.get_size()
        
        # the first ball
        ball1 = Ball("white", center, 5, self.screen, is_shot=True)
        ball1.shot(0, 0)
        ball1.display_ball()
        balls_lt.append(ball1)
        
        # the second ball
        ball2 = Ball("white", center, 5, self.screen, is_shot=True)
        ball2.shot(w/2, 0)
        ball2.display_ball()
        balls_lt.append(ball2)
        
        # the third ball
        ball3 = Ball("white", center, 5, self.screen, is_shot=True)
        ball3.shot(0, w)
        ball3.display_ball()
        balls_lt.append(ball3)
        
        return balls_lt

