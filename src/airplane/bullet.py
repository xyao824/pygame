import pygame
import os

IMAGE_PATH = 'image'

class Bullet(pygame.sprite.Sprite):

    def __init__(self, x, y, damage):
        super(Bullet, self).__init__()
        self.live=True
        self.speed = 10
        self.damage = damage
        self.image = pygame.image.load(f'{os.getcwd()}/{IMAGE_PATH}/bullet.png')
        self.rect = self.image.get_rect()
        # print(x)
        self.rect.x = x+15
        self.rect.y = y-10

    def hit_plane(self, screen, enemy_plane_list, bang_sound, total_score):
        for enemy_plane in enemy_plane_list:
            if pygame.sprite.collide_rect(self,enemy_plane):
                hit_image = pygame.image.load(f'{os.getcwd()}/{IMAGE_PATH}/hit.png')
                screen.blit(hit_image, (self.rect.x, self.rect.y))
                if enemy_plane.hp - self.damage <= 0:
                    enemy_plane.live = False
                    bang_sound.play()
                    total_score += enemy_plane.score
                else:
                    enemy_plane.hp -= self.damage
                self.live = False
        return total_score
    
    def bullet_move(self, screen):
        w, h = screen.get_size()

        if self.rect.y > 0:
            self.rect.y -= self.speed
        else:
            self.live = False

    def display_bullet(self, screen):
        screen.blit(self.image,self.rect)

