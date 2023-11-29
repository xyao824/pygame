import pygame
import time
from bullet import Bullet
from items import Item

IMAGE_PATH = '../image/'

class AirPlane(pygame.sprite.Sprite):
    def __init__(self,bang_sound, shot_sound):
        super(AirPlane, self).__init__()
        self.live=True
        self.hp = 100
        self.speed = 1
        self.bang_sound = bang_sound
        self.shot_sound = shot_sound
    # 加载图片
    def load_image(self, screen):
        if hasattr(self, 'image') and hasattr(self, 'rect'):
            screen.window.blit(self.image, self.rect)
        else:
            print("Error")

    def display_airplane(self, screen):
        screen.blit(self.image,self.rect)

class My_AirPlane(AirPlane):
    def __init__(self,x,y,hp,speed,bang_sound,shot_sound,life_remain):
        super().__init__(bang_sound, shot_sound)
        self.image = pygame.image.load(f'{IMAGE_PATH}/airplane.png')
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hp = hp
        self.speed = speed
        self.produce_shot = 25
        self.shot_count = 0
        self.total_score = 0
        self.life_remain = life_remain
        self.hitted = False

    def my_airplane_move(self, screen, move_x, move_y):
        #7 在屏幕范围内，实现移动
        w, h = screen.get_size()
        if move_y < 0 and self.rect.y <= 0:
            pass
        elif move_y > 0 and self.rect.y >= 900-36-5:
            pass
        elif move_x < 0 and self.rect.x <= 0:
            pass
        elif move_x > 0 and self.rect.x >= w-36:
            pass
        else:
            self.rect.y += move_y
            self.rect.x += move_x

    def shot(self, screen, bullet_lt, enemy_plane_list, damage):
        self.shot_count += 1
        if self.shot_count == self.produce_shot:
            bullet_lt.append(Bullet(self.rect.x, self.rect.y, damage))
            self.shot_sound.play()
            self.shot_count = 0

        for bullets in bullet_lt:
            if bullets.live:
                bullets.display_bullet(screen)
                bullets.bullet_move(screen)
                self.total_score = bullets.hit_plane(screen, enemy_plane_list, self.bang_sound, self.total_score)
            else:
                bullet_lt.remove(bullets)

        return self.total_score
    
    def hit_plane(self, enemy_plane_list, GAMEOVER):
        hitted = False
        for enemy_plane in enemy_plane_list:
            if pygame.sprite.collide_rect(self,enemy_plane):
                hitted = True
                self.live = False
                self.bang_sound.play()
                if self.life_remain > 0:
                    self.life_remain -= 1
                    return GAMEOVER, self.life_remain, hitted
                else:
                    GAMEOVER = True
        return GAMEOVER, self.life_remain, hitted
    
    def add_life(self):
        if self.live:
            self.life_remain += 1

    def upgrade_fire(self, bullet_damage):
        bullet_damage += 100
        if self.produce_shot > 5:
            self.produce_shot -= 5
        else:
            self.produce_shot = 5 # max speed
        
        if self.shot_count >= self.produce_shot:
            self.shot_count = self.produce_shot - 1

        return bullet_damage

    def destory_all_enemy(self, enemy_plane_list):
        self.bang_sound.play()
        for enempy_plane in enemy_plane_list:
            if enempy_plane.live:
                print(enempy_plane)
                self.total_score += enempy_plane.score
                enempy_plane.live = False
            else:
                enemy_plane_list.remove(enempy_plane)
        
        return enemy_plane_list
    
    
    def hit_item(self, items_list, enemy_plane_list, bullet_damage):
        for item in items_list:
            if pygame.sprite.collide_rect(self,item):
                item.live = False
                # upgrade sound play

                # mapping the item type with action
                if item.item_type == "pluslife":
                    # print("Added life")
                    self.add_life()
                elif item.item_type == "updatefire":
                    # print("Update fire")
                    self.upgrade_fire(bullet_damage)
                elif item.item_type == "destroyall":
                    # print("Destroy all")
                    enemy_plane_list = self.destory_all_enemy(enemy_plane_list)
        
        return self.life_remain, enemy_plane_list, bullet_damage

    def response(self, x, y):
        """
        overwrite
        """
        self.rect.x = x
        self.rect.y = y
        self.produce_shot = 25
        self.shot_count = 0
        self.live = True

class Enemy_Airplane(AirPlane):
    def __init__(self,image,x,y,speed,bang_sound, shot_sound, hp, score):
        super().__init__(bang_sound, shot_sound)
        self.image = pygame.image.load(f'{IMAGE_PATH}/{image}')
        self.rect = self.image.get_rect()
        self.rect.x = x  #should be a random number but can not exced my screen
        self.rect.y = y  #should be a random number but can not exced my screen
        self.speed = speed
        self.hp = hp
        self.score = score
    
    def enemy_airplane_move(self, screen):
        w, h = screen.get_size()
        
        if self.rect.y < 900:
            self.rect.y += self.speed
        else:
            self.live = False
    
