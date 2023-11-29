import pygame
import time
from random import randrange, uniform
from airplane import AirPlane, My_AirPlane, Enemy_Airplane
from items import Item

# golbal variables
IMAGE_PATH = '../image/'
MUSIC_PATH = '../music/'
# Mapping for myenemy airplanes
ENEMY_PLANE_LIST = [
    {"enemy_type":"enemy_airplane.png", "HP":100, "enemy_width": 36, "score": 100}, 
    {"enemy_type":"enemy_airplane_A.png", "HP":300, "enemy_width": 36, "score": 300},
    {"enemy_type":"enemy_airplane_B.png", "HP":500, "enemy_width": 144, "score": 500}
]
# Mapping for items
ITEMS_LIST = [
    {"item_image":"item_A.png", "item_type": "pluslife"}, # +1 life
    {"item_image":"item_B.png", "item_type": "updatefire"},  # + attack speed & damage
    {"item_image":"item_C.png", "item_type": "destroyall"} # clear all enemy
]

WIDTH = 720
HEIGHT = 1008

GAMEOVER = False
SOUND_ON = True
LIFE_REMAIN = 3

def set_up_mixer():
    pygame.mixer.init()
    background_sound = pygame.mixer.Sound(f"{MUSIC_PATH}sakura.wav")
    background_sound.set_volume(0.1)
    # background_sound.play(-1) # loop playing
    bang_sound          = pygame.mixer.Sound(f"{MUSIC_PATH}bang.wav")
    bang_sound.set_volume(0.1)
    shot_sound           = pygame.mixer.Sound(f"{MUSIC_PATH}eat.wav")
    shot_sound.set_volume(0.1)

    return bang_sound, shot_sound

def sound_button(screen, SOUND_ON):
    if SOUND_ON:
        button_image = pygame.image.load(f'{IMAGE_PATH}/sound.png')
    else:
        button_image = pygame.image.load(f'{IMAGE_PATH}/sound_off.png')
    button_rect = button_image.get_rect()
    button_rect.x = 650
    button_rect.y = 905
    screen.blit(button_image, button_rect)

    return button_rect

def create_item(screen, items_list):
    
    if randrange(1, 11) in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]: # 33% prduce items
        index = randrange(0, 3)
        x = randrange(0, WIDTH-36)
        item = Item(ITEMS_LIST[index]["item_image"], x = x, y = 0, item_type=ITEMS_LIST[index]["item_type"])
        items_list.append(item)
        

def create_enemy_airplane(screen, enemy_plane_list, bang_sound, shot_sound):
    # max enemy 720 / 36 = 20
    # min enemy 0

    """
    response enemy planes
        1. max enemy response one time 720 / 36*4 = 5
        2. min enemy 0
        3. the enemy response number is following by time
        4. difference plan has different speed
        5. respone enemy can not exced the screen width
    """
    x_list = []

    for i in range(0, randrange(0, 6)):
        speed = round(uniform(1,5), 1)
        index = randrange(0,3)
        enemy_plane_type = ENEMY_PLANE_LIST[index]["enemy_type"]
        hp = ENEMY_PLANE_LIST[index]['HP']
        x  = randrange(0, WIDTH, 36)
        if x not in x_list and (x + ENEMY_PLANE_LIST[index]["enemy_width"]) <= WIDTH: # can not repeat
            enemy_airplane = Enemy_Airplane(image =enemy_plane_type, x = x, y = 0, speed = speed, bang_sound=bang_sound, shot_sound = shot_sound, hp = hp, score = ENEMY_PLANE_LIST[index]["score"])
            enemy_plane_list.append(enemy_airplane)
            x_list.append(x)
    
    return randrange(10, 100, 20)

def draw_background(surface):
    light_gray = (211, 211, 211)
    surface.fill(light_gray)
    moon_image = pygame.image.load(f'{IMAGE_PATH}/moon.png')
    large_moon_image = pygame.image.load(f'{IMAGE_PATH}/large_moon.png')
    asteroid_image = pygame.image.load(f'{IMAGE_PATH}/asteroid.png')
    surface.blit(moon_image, (123, 456))
    surface.blit(moon_image, (78, 612))
    surface.blit(moon_image, (62, 73))
    surface.blit(large_moon_image, (311, 78))
    surface.blit(large_moon_image, (444, 250))
    surface.blit(large_moon_image, (444, 570))
    surface.blit(asteroid_image, (555, 371))
    surface.blit(asteroid_image, (225, 225))
    surface.blit(asteroid_image, (412, 812))

def draw_map(surface):
    gray = (128, 128, 128)
    start_point = (0, 900)
    end_point = (720, 900)
    line_width = 10
    pygame.draw.line(surface, gray, start_point, end_point, line_width)
    button_image = pygame.image.load(f'{IMAGE_PATH}/bottom.png')
    surface.blit(button_image, (0, 900))

def draw_text(content, size, color):
    pygame.font.init()
    font = pygame.font.SysFont('kaiti', size)
    text = font.render(content, True, color)
    return text

def log_life(screen, life_remain):
    my_plane_image =  pygame.image.load(f'{IMAGE_PATH}/airplane.png')
    screen.blit(my_plane_image, (0, 930))
    text = draw_text(f" X  {life_remain}", 30, (0, 0, 0))
    screen.blit(text, (40, 940))

def log_source(score, screen):
    text = draw_text(f"score: {score}", 26, (0, 0, 0))
    screen.blit(text, (5, 905))

def main(SOUND_ON, GAMEOVER, LIFE_REMAIN):
    GAMEOVER=GAMEOVER
    SOUND_ON=SOUND_ON
    # init the mixter
    bang_sound, shot_sound = set_up_mixer()
    # init the game screen size
    pygame.init()
    speed = 1
    # plane size should be 36*36 pixel
    pygame.display.set_caption('airplane game')

    enemy_plane_list = []
    bullet_damage = 100
    bullet_lt = []
    items_list = []
    count_enemy_plane = 0
    produce_enemy_plane = 50 # wairing start
    count_item = 0
    produce_item = 500
    total_score = 0

    size = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(size)
    #Add my airplane
    my_airplane = My_AirPlane(x = 360-18, y = 900-36-5, hp =100, speed = speed, bang_sound=bang_sound, shot_sound=shot_sound, life_remain=LIFE_REMAIN)

    while not GAMEOVER:
        # button_rect = sound_button(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GAMEOVER = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the mouse click is within the button rectangle
                if button_rect.collidepoint(event.pos):
                    if SOUND_ON:
                        SOUND_ON = False
                        # turn off the sound
                        bang_sound.set_volume(0)
                        shot_sound.set_volume(0)
                        # show sound off image
                        sound_button(screen, SOUND_ON)
                        
                    else:
                        SOUND_ON = True
                        # turn on the sound
                        bang_sound.set_volume(0.1)
                        shot_sound.set_volume(0.1)
                        # show sound on image
                        sound_button(screen, SOUND_ON)

        draw_background(screen)
        #  create enemy airplane
        count_enemy_plane += 1
        if count_enemy_plane == produce_enemy_plane:
            produce_enemy_plane = create_enemy_airplane(screen, enemy_plane_list, bang_sound, shot_sound)
            count_enemy_plane = 0
        
        # create the items in every 500 time
        count_item +=1
        if count_item == produce_item:
            create_item(screen, items_list)
            count_item = 0
        # Control my airplane
        keys_pressed = pygame.key.get_pressed()
        
        if keys_pressed[pygame.K_w]:
            move_y = -5 * speed
            my_airplane.my_airplane_move(screen, move_x=0, move_y=move_y)

        if keys_pressed[pygame.K_s]:
            move_y = 5 * speed
            my_airplane.my_airplane_move(screen, move_x=0, move_y=move_y)

        if keys_pressed[pygame.K_a]:
            move_x = -5 * speed
            my_airplane.my_airplane_move(screen, move_x=move_x, move_y=0)

        if keys_pressed[pygame.K_d]:
            move_x = 5 * speed
            my_airplane.my_airplane_move(screen, move_x=move_x, move_y=0)

        my_airplane.display_airplane(screen)
        total_score = my_airplane.shot(screen, bullet_lt, enemy_plane_list, damage = bullet_damage)
        #  Adding enemy planes to screen
        for enemy_airplane in enemy_plane_list:
            if enemy_airplane.live:
                enemy_airplane.display_airplane(screen)
                enemy_airplane.enemy_airplane_move(screen)
                
            else:
                enemy_plane_list.remove(enemy_airplane)
        # Adding items to screen
        for item in items_list:
            if item.live:
                item.display_item(screen)
                item.item_move(screen)
            else:
                items_list.remove(item)
        draw_map(screen)
        log_source(total_score, screen)
        log_life(screen, LIFE_REMAIN)
        button_rect = sound_button(screen, SOUND_ON)
        GAMEOVER, LIFE_REMAIN, hitted= my_airplane.hit_plane(enemy_plane_list, GAMEOVER)
        LIFE_REMAIN, enemy_plane_list, bullet_damage = my_airplane.hit_item(items_list, enemy_plane_list, bullet_damage)
        if hitted:
            bullet_damage = 100
            items_list = []
            enemy_plane_list = []
            my_airplane.response(360-18, 900-36-5) 
            my_airplane.display_airplane(screen)
        pygame.display.update()
        pygame.time.Clock().tick(60)

if __name__ == '__main__':
    main(SOUND_ON, GAMEOVER, LIFE_REMAIN)