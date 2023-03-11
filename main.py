import random
from os import listdir

import pygame
from pygame. constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

FPS = pygame.time.Clock()

screen = width, heigth = 800, 600

BLACK = 0, 0, 0
WHILE = 255, 255, 255
RED = 255, 0, 0
BLUE = 102, 255, 255

font = pygame.font.SysFont('Verdana', 20)

main_surface = pygame.display.set_mode(screen)

IMGS_PATH = 'goose'

player_imgs = [pygame.image.load(IMGS_PATH + '/' + file).convert_alpha() for file in listdir(IMGS_PATH)]
ball = player_imgs[0]
bail_rect = ball.get_rect()
bail_speed = 5

def create_enemy():
    enemy = pygame.transform.scale(pygame.image.load('enemy.png').convert_alpha(), (75, 35))
    enemy_rect = pygame.Rect(width, random.randint(0, heigth), *enemy.get_size())
    enemy_speed = random.randint(4, 6)        

    return [enemy, enemy_rect, enemy_speed]

def create_bonus():
    bonus =pygame.transform.scale(pygame.image.load('bonus.png').convert_alpha(), (50,100))
    bonus_rect = pygame.Rect(random.randint(0, width), 0, *bonus.get_size())
    bonus_speed = random.randint(4, 6)
    return [bonus, bonus_rect, bonus_speed]

bg = pygame.transform.scale(pygame.image.load('background.png').convert(), screen )
bgX = 0
bgX2 = bg.get_width()
bg_speed = 3

CREATE_ENENY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENENY, 1500)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 2500)

CHANCHE_IMG = pygame.USEREVENT + 3
pygame.time.set_timer(CHANCHE_IMG, 125)

enemies = []
bonuses = []
scores = 0

img_index =0
is_working = True

while is_working:

    FPS.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT :
            is_working = False 

        if event.type ==  CREATE_ENENY:
            enemies.append(create_enemy())     
            
        if event.type ==  CREATE_BONUS:
            bonuses.append(create_bonus())     

        if event.type ==  CHANCHE_IMG:
            img_index += 1
            if img_index == len(player_imgs):
                img_index = 0
            ball = player_imgs[img_index]

    pressent_keys = pygame.key.get_pressed()

    # main_surface.fill(WHILE)

    # main_surface.blit(bg, (0, 0))

    bgX -= bg_speed
    bgX2 -= bg_speed

    if bgX < -bg.get_width():
        bgX = bg.get_width()

    if bgX2 < -bg.get_width():
        bgX2 = bg.get_width()

    main_surface.blit(bg, (bgX, 0))
    main_surface.blit(bg, (bgX2, 0))

    main_surface.blit(ball, bail_rect)

    main_surface.blit(font.render(str(scores), True, RED), (width -30, 0))

    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2], 0)
        main_surface.blit(enemy[0], enemy[1])

        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

        if enemy[1].bottom >= heigth:
             enemy[1] = enemy[1].move(0, enemy[2]) 
             
        if enemy[1].top <= 0:
             enemy[1] = enemy[1].move(0, -enemy[2]) 

        if bail_rect.colliderect(enemy[1]):
           is_working = False

    
    for bonus in bonuses:
        bonus[1] = bonus[1].move(0, bonus[2])
        main_surface.blit(bonus[0], bonus[1])

        if bonus[1].bottom >= heigth:
            bonuses.pop(bonuses.index(bonus))

        if bonus[1].left <= 0:
             bonus[1] = bonus[1].move(-bonus[2], 0) 
             
        if bonus[1].right >= width:
             bonus[1] = bonus[1].move(bonus[2], 0) 

        if bail_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            scores += 1

    if pressent_keys[K_DOWN] and not bail_rect.bottom >= heigth: 
          bail_rect = bail_rect.move(0, bail_speed)        

    if pressent_keys[K_UP] and not bail_rect.top <= 0: 
        bail_rect = bail_rect.move(0, -bail_speed)    

    if pressent_keys[K_LEFT] and not bail_rect.left <= 0: 
        bail_rect = bail_rect.move(-bail_speed, 0)    

    if pressent_keys[K_RIGHT] and not bail_rect.right >= width: 
        bail_rect = bail_rect.move(bail_speed, 0)    

    # print(len(enemies))

    # main_surface.fill((155, 155, 155))
    pygame.display.flip()