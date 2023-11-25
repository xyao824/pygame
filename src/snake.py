class Point:
    def __init__(self, direction, row, col):
        self.direction = direction
        self.row = row
        #print(self.row)
        self.col = col
        #print(self.col)
    def copy(self):
        return Point(direction = self.direction, row=self.row, col = self.col)
import pygame
import sys
from random import randrange
from random import choice
from collections import defaultdict
def rect(point, color, box_wide, box_height):
    #print(point.row, point.col)
    x = point.col * box_wide
    y = point.row * box_height
    #print(x, y)
    pygame.draw.rect(window, color, (x, y, box_wide, box_height))
#pygame.mixer.pre_init(44100,16,2,4096)
pygame.mixer.init()
background_sound = pygame.mixer.Sound(r"..\music\sakura.wav")
background_sound.set_volume(1)
background_sound.play(-1) # loop playing
bang_sound          = pygame.mixer.Sound(r"..\music\bang.wav")
#bang_sound.set_volume(1)
eat_sound           = pygame.mixer.Sound(r"..\music\eat.wav")
pygame.init()
wide = 800
height = 600
bg_color = (66, 245, 245)
snake_color =(128, 128, 128)
row = 40 #the size for the frame
col = 50
direction = 2
sorce = 0
time = row*col/200 
snake = [Point(direction = 2, row = int(row/2), col = int(col/2)-1),
         Point(direction = 2, row = int(row/2), col = int(col/2)-2)]
ok = True
box_wide = wide/col
box_height = height/row
#print(box_wide)
#print(box_height)
size = (wide, height)
window = pygame.display.set_mode(size)
pygame.display.set_caption('greely snake')
head = Point(direction = direction, row = int(row/2), col = int(col/2))
head_color = (0, 0, 0)
food = Point(direction = 0,row=randrange(row), col=randrange(col))
food_color=(255, 255, 0)
game_quit= True
death = False
clock = pygame.time.Clock()
while game_quit:
    snake.insert(0, head.copy())
    snake.pop()
    if direction == 1:
        head.row -= 1
    elif direction == 2:
        head.col += 1
    elif direction == 3:
        head.row += 1
    elif direction == 4:
        head.col -= 1
    for event in pygame.event.get():
        #print(event)
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                #print(direction)
                if direction != 2 and direction != 4:
                    direction = 4
                    #print("left", direction)
            if event.key == pygame.K_RIGHT:
                if direction != 2 and direction != 4:
                    direction = 2
                    #print("right", direction)
            if event.key == pygame.K_UP:
                if direction != 1 and direction != 3:
                    direction = 1
                    #print("up",  direction)
            if event.key == pygame.K_DOWN:
                if direction != 1 and direction != 3:
                    direction = 3
                    #print("down", direction)
    #if snake eat the food
    if int((head.col * box_wide + box_wide/2)+(head.row * box_height + box_height/2)) == int((food.col * box_wide + box_wide/2)+(food.row * box_height + box_height/2)): #判定点设置在蛇头的中心//食物的中心
        #print("yumi")
        sorce += 100
        #print(sorce)
        eat_sound.play()
        # the snake grows up 动态规划 每一个方块跟随它前一个的运动轨迹
        if direction == 1: 
            snake.append(Point(direction, head.row+1, head.col))
            #print(snake)
        elif direction == 2:
            snake.append(Point(direction, head.row, head.col-1))
            #print(snake)
        elif direction == 3:
            snake.append(Point(direction, head.row-1, head.col))
            #print(snake)
        elif direction == 4:
            snake.append(Point(direction, head.row, head.col+1))
            #print(snake)

        # 食物不能刷新在蛇头/身上 (not done)
        #food_row = choice([i for i in range(1, row-1) if i not in [element.row for element in snake]])
        #food_col = choice([i for i in range(1, col-1) if i not in [element.col for element in snake]])
        food_row = randrange(1, row-1)
        food_col = randrange(1, row-1)
        food = Point(direction = 0, row=food_row, col=food_col) #食物刷新
        #控制蛇的速度 base on the sorce
        time = time + (sorce/100)/20
    pygame.draw.rect(window, bg_color, (0, 0, wide, height))
    for element in snake:
        #print(element)
        rect(element, snake_color, box_wide, box_height)
        if head.col == element.col and head.row == element.row:
            death = True
            bang_sound.play()
    ## 死亡

    if head.col * box_wide + box_wide/2 <= 0 or head.row * box_height + box_height/2 <= 0 or head.col * box_wide + box_wide/2 >= wide or head.row * box_height + box_height/2>= height:
        bang_sound.play()
        death = True
    if death:
        print("game over")
        game_quit = False
        background_sound.stop()
    rect(head, head_color, box_wide, box_height)
    rect(food, food_color, box_wide, box_height)
    pygame.display.flip()
    clock.tick(time) #控制蛇的速度


if __name__ == "__main__":
    main() 