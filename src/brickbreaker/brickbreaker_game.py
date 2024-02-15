import pygame
import sys
from PIL import Image
import os 
import fnmatch
from brick import Brick, Wall, Block
from button import Button
from bar import Bar
from ball import Ball
from random import randrange, uniform


# golbal variables
IMAGE_PATH = '/image'
MUSIC_PATH = '/music'
MAP_PATH = '/map'


MAP_WIDTH = 720
MAP_HEIGHT = 600

SCREEN_WIDTH = 720
SCREEN_HEIGHT = 1008
SPEED = 1

EXIT = False
GAMEOVER = False
SOUND_ON = True

def choose_map(screen, EXIT):
    """
    Allow use to choose map
    """
    map_choosed = False
    map_name = "level1.txt"
    
    while not map_choosed and not EXIT:
        map_dct = {}
        index = 0
        mouse_x, mouse_y = pygame.mouse.get_pos()
        light_yellow = (255, 255, 237)
        w, h = screen.get_size()
        button_width = 150
        width_gap = (w%button_width / ((w//button_width)+1))
        button_height = 120
        height_gap = (h%button_height / ((h//button_height)+1))

        draw_background(screen, light_yellow)
        total_maps = len(fnmatch.filter(os.listdir(f'{os.getcwd()}/{MAP_PATH}'), '*.txt'))
        for width in range(0, w//button_width):
            for height in range(0, h//button_height):
                index += 1
                if index <= total_maps:
                    level_button = draw_button(
                        screen=screen,
                        mouse_x=mouse_x,
                        mouse_y=mouse_y,
                        post_x= width_gap * (width+1) + button_width * width,
                        post_y= height_gap * (height+1) + button_height * height,
                        button_text=f'Level{index}',
                        button_color= (255, 255, 0),
                        hovering_color=(204, 204, 0),
                        button_width= button_width,
                        button_height= button_height)
                    map_dct[f'level{index}.txt'] = level_button


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                EXIT = True
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for key, value in map_dct.items():
                    if value.is_hovering_button(mouse_x = mouse_x, mouse_y = mouse_y):
                        map_choosed = True
                        map_name = key
        pygame.display.flip()
        pygame.time.Clock().tick(60)

    return map_name

def draw_button(screen,  
                mouse_x, 
                mouse_y, 
                post_x, 
                post_y,
                button_text,
                button_color,
                hovering_color,
                button_width,
                button_height):
    """
    draw button on the screen, changed the color when mouse hovering on
    """
    button = Button(screen=screen, 
                    width=button_width, 
                    height= button_height, 
                    post_x= post_x, 
                    post_y=post_y,
                    color=button_color)
    
    button.hovering_button(hovering_color, mouse_x, mouse_y) 
    button.display_button()

    text, font = draw_text(button_text, 30, (0, 0, 0))
    text_width, text_height = font.size(button_text)
    screen.blit(text, (post_x+(button_width-text_width)/2, post_y+(button_height-text_height)/2))

    return button

def draw_text(content, size, color):
    """
    draw text
    """
    pygame.font.init()
    font = pygame.font.SysFont('kaiti', size)
    text = font.render(content, True, color)
    return text, font

def draw_map(map, brick_size, screen):
    """
    draw map based on the readed map
    """
    bricks_lt = []
    walls_lt = []
    
    for row_index in range(0, len(map)):
        for item_index in range(0, len(map[row_index])):
            if map[row_index][item_index] == 1: # brick
                bricks_lt.append(Brick(item_index*brick_size[0], row_index*brick_size[1], screen))
            elif map[row_index][item_index] == 2: # wall
                walls_lt.append(Wall(item_index*brick_size[0], row_index*brick_size[1], screen))
            else:
                pass #None
    return bricks_lt, walls_lt

def draw_background(screen, background_color):
    """
    draw background color for each screen
    """
    screen.fill(background_color)
    
def read_map(filename):
    '''
    read map from the input file
    '''
    with open(f'{os.getcwd()}/{MAP_PATH}/{filename}', 'r') as f:
        l = [[int(num) for num in line.split(',')] for line in f]
    
    im = Image.open(f'{os.getcwd()}/{IMAGE_PATH}/brick.png')
    # pix = im.load() change the image color/shape

    if len(l[0]) != MAP_WIDTH/im.size[0] or len(l) != MAP_HEIGHT/im.size[1]:
        raise Exception("Sorry, error when loading the map")
    else:
        return l, im.size

def load_gameover(screen, w, h, mouse_x, mouse_y):
    """
    print the game over text and set the GAMEOVER to True
    """
    light_red = (255, 127, 127)
    draw_background(screen, light_red)
    text, font = draw_text("GameOver", 30, (0, 0, 0))
    text_width, text_height = font.size("GameOver")

    screen.blit(text, ((w-text_width)//2, h//2))
    
    button_width = 150
    button_height = 50
    button_color = (144, 238, 144)
    hovering_color = (0, 128, 0)
    post_x = (w-button_width)//2
    post_y =  h//2+100
    restart_button = draw_button(screen,
                                 mouse_x,
                                 mouse_y,
                                 post_x,
                                 post_y,
                                 button_text="Restart",
                                 button_color=button_color,
                                 hovering_color=hovering_color,
                                 button_width=button_width,
                                 button_height=button_height)
    
    button_color = (0, 255, 255)
    hovering_color = (137, 207, 240)
    exit_button = draw_button(screen,
                              mouse_x,
                              mouse_y,
                              post_x,
                              post_y = h//2+200,
                              button_text="Exit",
                              button_color=button_color,
                              hovering_color=hovering_color,
                              button_width=button_width,
                              button_height=button_height)
    return restart_button, exit_button

def main(SOUND_ON, GAMEOVER, EXIT):
    EXIT = EXIT
    GAMEOVER=GAMEOVER
    SOUND_ON=SOUND_ON
    size = (SCREEN_WIDTH, SCREEN_HEIGHT)
    screen = pygame.display.set_mode(size)
    w, h = screen.get_size()
    map_name = choose_map(screen, EXIT)
    map, brick_size = read_map(filename = map_name)
    balls_lt = [] 
    item_lt = []
    bricks_lt, walls_lt = draw_map(map, brick_size, screen)
    
    # init the bar
    bar = Bar(312, 960, screen, "bar.png")
    bar.display_bar()
    

    # init the ball
    init_ball = Ball("white", (bar.rect.center[0], bar.rect.center[1]-17), 5, screen)
    live_ball_count = 1
    balls_lt.append(init_ball)
    

    while not EXIT:
        # button_rect = sound_button(screen)
        # update background
        light_gray = (211, 211, 211)
        draw_background(screen, light_gray)
        # display bricks
        for brick in bricks_lt:
            if brick.live:
                brick.display_block()
        # display walls
        for wall in walls_lt:
            wall.display_block()
        # move bar following the mouse post
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if live_ball_count == 0:
            GAMEOVER = True
            restart_button, exit_button = load_gameover(screen, w, h, mouse_x, mouse_y)
        elif len(walls_lt) == 0:
            GAMEOVER = True
        else:
            live_ball_count = 0
            for index in range (0, len(balls_lt)):

                ball = balls_lt[index]
                live_ball_count += ball.live
                if ball.is_shot and ball.live:
                    bar.move_bar(mouse_x)
                    bar.display_bar()
                    new_center = ball.move_ball()
                    ball.display_ball()
                    ball.get_angle_ball()
                    # If the ball goes out of the bottom, pop the ball from the ball list
                    if new_center[1] >= h - 24:
                        ball.live = False
                        continue

                    hitted = bar.hit_ball(ball)
                    for block in bricks_lt:
                        if block.live:
                            item_lt = block.hit_ball(ball = ball, items_lt = item_lt)
                    for block in walls_lt:
                            item_lt = block.hit_ball(ball = ball, items_lt = item_lt)
                elif not ball.is_shot:    
                    ball = Ball("white", (bar.rect.center[0], bar.rect.center[1]-17), 5, screen)
                    ball.display_ball()
                    bar.display_bar()
            for item in item_lt:
                if item.live:
                    item.display_item()
                    item.item_fall()
                    balls_lt, bar = bar.hit_item(item, ball, balls_lt)
                else:
                    item_lt.remove(item)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                EXIT = True
            # only do once
            elif event.type == pygame.MOUSEBUTTONDOWN and not init_ball.is_shot:
                init_ball.shot(mouse_x, mouse_y)
            elif GAMEOVER and event.type == pygame.MOUSEBUTTONDOWN:
                if restart_button.is_hovering_button(mouse_x = mouse_x, mouse_y = mouse_y):
                    main(SOUND_ON, GAMEOVER=False, EXIT=False)
                elif exit_button.is_hovering_button(mouse_x = mouse_x, mouse_y = mouse_y):
                    EXIT = True
            # # Check if the mouse click is within the button rectangle
            #     if button_rect.collidepoint(event.pos):
            #         if SOUND_ON:
            #             SOUND_ON = False
            #             # turn off the sound
            #             bang_sound.set_volume(0)
            #             shot_sound.set_volume(0)
            #             # show sound off image
            #             sound_button(screen, SOUND_ON)
                        
            #         else:
            #             SOUND_ON = True
            #             # turn on the sound
            #             bang_sound.set_volume(0.1)
            #             shot_sound.set_volume(0.1)
            #             # show sound on image
            #             sound_button(screen, SOUND_ON)
        pygame.display.flip()
        pygame.time.Clock().tick(60)
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    pygame.init()
    main(SOUND_ON, GAMEOVER, EXIT)