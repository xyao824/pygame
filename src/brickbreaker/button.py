import pygame
import os


class Button(pygame.sprite.Sprite):
    def  __init__(self, screen, width, height, post_x, post_y, color):

        self.screen = screen
        self.width = width
        self.height = height
        self.post_x = post_x
        self.post_y = post_y
        self.color = color
        self.draw_button()

    def draw_button (self):
        """
        draw button
        """
        w, h = self.screen.get_size()
        self.button = pygame.Rect(self.post_x, self.post_y, self.width, self.height)

    def display_button(self):
        """
        display button on screen
        """
        pygame.draw.rect(self.screen, self.color, self.button)
    
    def is_hovering_button(self, mouse_x, mouse_y):
        """
        return true when mouse hovering the button and
        """

        if self.button.topleft[0] <= mouse_x <= self.button.topright[0] and \
            self.button.topleft[1] <= mouse_y <= self.button.bottomleft[1]:
        
            return True

        return False
    
    def hovering_button(self, color, mouse_x, mouse_y):
        """
        changing the color when mouse hovering the button
        """

        if self.is_hovering_button(mouse_x, mouse_y):
            self.color = color