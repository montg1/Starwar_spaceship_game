from asyncio import shield
from pickle import FALSE
from cv2 import FONT_HERSHEY_COMPLEX
import pygame
import os
import threading
import time
import random
import socket
import sys
from time import *

pygame.font.init()
pygame.mixer.init()

clientNumber = 0

WIDTH, HEIGHT = 1080, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (0, 255, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Grenade+1.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/Gun+Silencer.mp3')

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60
speed = 5
imortal = True
BULLET_speed = 10
MAX_BULLETS = 4
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 75, 75
Tie_Fighter_Width,Tie_Fighter_Height = 50, 100

TIE_FIGHTER_HIT = pygame.USEREVENT + 1
X_WING_HIT = pygame.USEREVENT + 2
DOGE = pygame.USEREVENT +1

TIE_FIGHTER_IMAGE = pygame.image.load(
    os.path.join('starwarship', 'Tie-Fighter.png'))
TIE_FIGHTER = pygame.transform.rotate(pygame.transform.scale(
    TIE_FIGHTER_IMAGE, (Tie_Fighter_Width,Tie_Fighter_Height)), 90)

X_WING_IMAGE = pygame.image.load(
    os.path.join('starwarship', 'X_Wing.png'))
X_WING = pygame.transform.rotate(pygame.transform.scale(
    X_WING_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('starwarship', 'space.gif')), (WIDTH, HEIGHT))

SHIELD_IMAGE = pygame.image.load(
    os.path.join("starwarship","ShieldHit.png"))
SHIELD =pygame.transform.rotate(pygame.transform.scale(
    SHIELD_IMAGE, (120, 120)), 0)

#Missile_IMAGE= pygame.image.load(os.path.join("starwarship","missile.png"))
#Missile = pygame.transform.rotate(pygame.transform.scale(
    #Missile_IMAGE, (Tie_Fighter_Width,Tie_Fighter_Height)), 0)

def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health, shield_hit_Tie, shield_hit_X):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render(
        "Energy Shield: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render(
        "Energy Shield: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(TIE_FIGHTER, (yellow.x, yellow.y))
    WIN.blit(X_WING, (red.x, red.y))
    WIN.blit(SHIELD, (shield_hit_Tie.x, shield_hit_Tie.y))
    WIN.blit(SHIELD, (shield_hit_X.x, shield_hit_X.y))
    #WIN.blit(Missile,(red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

def draw_shield_hit(shield_hit):
    WIN.blit(SHIELD, (shield_hit.x, shield_hit.y))
    pygame.display.update()



def Tie_Fighter_movement(keys_pressed, yellow, speed, imortal):

    if keys_pressed[pygame.K_LSHIFT]:
        speed = 15
        imortal = False
        #pygame.event.post(pygame.event.Event(DOGE))
        #print(speed,"  ",imortal)
        #pygame.time.set_timer(DOGE, 3000)


    if keys_pressed[pygame.K_a] and yellow.x - speed > 0:  # LEFT
        yellow.x -= speed
    if keys_pressed[pygame.K_d] and yellow.x + speed + yellow.width < BORDER.x:  # RIGHT
        yellow.x += speed
    if keys_pressed[pygame.K_w] and yellow.y - speed > 0:  # UP
        yellow.y -= speed
    if keys_pressed[pygame.K_s] and yellow.y + speed + yellow.height < HEIGHT - 15:  # DOWN
        yellow.y += speed

def Tie_Figther_shield_Movement(keys_pressed, shield_hit_Tie):
    if keys_pressed[pygame.K_a] and shield_hit_Tie.x - speed > 0:  # LEFT
        shield_hit_Tie.x -= speed
    if keys_pressed[pygame.K_d] and shield_hit_Tie.x + speed + shield_hit_Tie.width < BORDER.x:  # RIGHT
        shield_hit_Tie.x += speed
    if keys_pressed[pygame.K_w] and shield_hit_Tie.y - speed > 0:  # UP
        shield_hit_Tie.y -= speed
    if keys_pressed[pygame.K_s] and shield_hit_Tie.y + speed + shield_hit_Tie.height < HEIGHT - 15:  # DOWN
        shield_hit_Tie.y += speed
    



def X_Wing_Movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - speed > BORDER.x + BORDER.width:  # LEFT
        red.x -= speed
    if keys_pressed[pygame.K_RIGHT] and red.x + speed + red.width < WIDTH:  # RIGHT
        red.x += speed
    if keys_pressed[pygame.K_UP] and red.y - speed > 0:  # UP
        red.y -= speed
    if keys_pressed[pygame.K_DOWN] and red.y + speed + red.height < HEIGHT - 15:  # DOWN
        red.y += speed

def X_Wing_shield_Movement(keys_pressed, shield_hit_X):
    if keys_pressed[pygame.K_LEFT] and shield_hit_X.x - speed > BORDER.x + BORDER.width:  # LEFT
        shield_hit_X.x -= speed
    if keys_pressed[pygame.K_RIGHT] and shield_hit_X.x + speed + shield_hit_X.width < WIDTH:  # RIGHT
        shield_hit_X.x += speed
    if keys_pressed[pygame.K_UP] and shield_hit_X.y - speed > 0:  # UP
        shield_hit_X.y -= speed
    if keys_pressed[pygame.K_DOWN] and shield_hit_X.y + speed + shield_hit_X.height < HEIGHT - 15:  # DOWN
        shield_hit_X.y += speed

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_speed
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(X_WING_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_speed
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(TIE_FIGHTER_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)
    

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)


def main():
    red = pygame.Rect(900, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    shield_hit_Tie = pygame.Rect(90, 268, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    shield_hit_X = pygame.Rect(890, 277, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 4
    yellow_health = 4
    bullet_position = 0
    bullet_position_X = 0
    imortal = True
    speed = 5

    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    if len(yellow_bullets) % 2 == 0: bullet_position = 10
                    else: bullet_position = 20
                    bullet = pygame.Rect(
                        yellow.x + yellow.width, yellow.y + yellow.height//2 - bullet_position, 10, 5) #-2 should be 20 and 10
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    if len(red_bullets) % 2 == 0: bullet_position_X = 30
                    else: bullet_position_X = -30
                    bullet = pygame.Rect(
                        red.x, red.y + red.height//2 - bullet_position_X, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            print(speed,"  ",imortal)

            if event.type == X_WING_HIT and imortal == True:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            elif imortal == False: red_health +=0

            if event.type == TIE_FIGHTER_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()
            elif imortal == False: red_health +=0

        winner_text = ""
        if red_health < 0:
            winner_text = "Yellow Wins!"

        if yellow_health < 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        Tie_Fighter_movement(keys_pressed, yellow, speed, imortal)
        Tie_Figther_shield_Movement(keys_pressed, shield_hit_Tie)
        X_Wing_Movement(keys_pressed, red)
        X_Wing_shield_Movement(keys_pressed, shield_hit_X)
        
        handle_bullets(yellow_bullets, red_bullets, yellow, red)


        draw_window(red, yellow, red_bullets, yellow_bullets,red_health,yellow_health,shield_hit_Tie,shield_hit_X)
        #print(threading.active_count())
        #print(threading.enumerate())
        
    main()


if __name__ == "__main__":
    main()