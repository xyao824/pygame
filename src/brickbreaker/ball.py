import pygame
import math

class Ball(pygame.sprite.Sprite):

    def __init__(self, color, center, radius, screen, is_shot=False, x_speed = 0, y_speed = 0):

        self.color = color
        self.center = center
        self.radius = radius
        self.screen = screen
        self.is_shot = is_shot
        self.live = True
        self.speed = 10
        self.x_speed = x_speed
        self.y_speed = y_speed
        self.angle = 0
    
    def display_ball(self):
        """
        Draw the ball in the screen
        """
        pygame.draw.circle(self.screen, self.color, self.center, self.radius)

    
    def shot(self, mouse_x, mouse_y):
        """
        shot the ball based on the postiton given
        """
        self.is_shot = True

        # calculate the x, y speed
        a = mouse_x - self.center[0]
        b = mouse_y - self.center[1]

        c = math.sqrt(a ** 2 + b ** 2)
        self.x_speed = (10/c)*a
        self.y_speed = (10/c)*b
    
    def move_ball(self):
        """
        move the ball in the screen
        """
        w, h = self.screen.get_size()
        new_center = [self.center[0] + self.x_speed, self.center[1] + self.y_speed]

        if 0 < new_center[0] < w and 0 < new_center[1] < h - 24:
            # Ball is within the screen boundaries, continue moving
            self.center = tuple(new_center)
        else:
            # Handle bouncing off screen boundaries
            if new_center[0] <= 0 or new_center[0] >= w:
                self.x_speed = -self.x_speed
            if new_center[1] <= 0:
                self.y_speed = -self.y_speed

            # Update the ball's position after bouncing
            self.center = (self.center[0] + self.x_speed, self.center[1] + self.y_speed)

            # If the ball reaches the corners, reverse both x and y speeds
            if (new_center[0], new_center[1]) in [(0, 0), (0, h - 24), (w, 0), (w, h - 24)]:
                self.x_speed = -self.x_speed
                self.y_speed = -self.y_speed

        return new_center

    def get_angle_ball(self):    
        """
        Get the ball move angle based on the x_speed and y_speed (angle with y-axis)
        """
        if self.x_speed == 0:
            if self.y_speed < 0:
                self.angle = 90.0
            else:
                self.angle = 270.0
        else:
            angle_radians = math.atan(abs(self.y_speed) / abs(self.x_speed))
            if self.y_speed <= 0 and self.x_speed < 0:
                self.angle = math.degrees(angle_radians)
            elif self.y_speed <= 0 and self.x_speed > 0:
                self.angle = 180.0 - math.degrees(angle_radians)
            elif self.y_speed >= 0 and self.x_speed > 0:
                self.angle = 180.0 + math.degrees(angle_radians)
            elif self.y_speed >= 0 and self.x_speed < 0:
                self.angle = 360.0 - math.degrees(angle_radians)  # Adjust for quadrant IV
    
    def split_ball(self, split_angle):
        """
        Get the split ball based on the current ball position and direction
        """
        new_angle = (self.angle + split_angle) % 360
        angle_radians = math.radians(new_angle)
        new_horizontal_speed = self.speed * math.cos(angle_radians)
        new_vertical_speed = self.speed * math.sin(angle_radians)

        split_ball = Ball("white", 
                         center=self.center, 
                         radius=5, 
                         screen=self.screen, 
                         is_shot=True,
                         x_speed=-new_horizontal_speed,
                         y_speed=-new_vertical_speed)
        split_ball.display_ball()
        
        return split_ball

    def times_threeballs(self, balls_lt):
        """
        +2 balls for each ball in the screen
        """
        new_balls_lt = []
        for ball in balls_lt: # Initialize a new list to store the new balls
                if ball.live:
                    ball.get_angle_ball()
                    new_balls_lt.append(ball.split_ball(60))
                    new_balls_lt.append(ball)
                    new_balls_lt.append(ball.split_ball(-60))
        return new_balls_lt



