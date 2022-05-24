import pygame
import os

class Tie_Figther:
    SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 50, 100
    VEL = 5
    BULLET_VEL = 10
    MAX_BULLETS = 40

    Tie_Fighter_Image = pygame.image.load(
        os.path.join('starwarship', 'Tie-Fighter.png'))
    Tie_Fighter_ship = pygame.transform.rotate(pygame.transform.scale(
        Tie_Fighter_Image, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

    def Tie_Figther_Movement(keys_pressed, TieFigther, BORDER, HEIGHT):
        if keys_pressed[pygame.K_a] and TieFigther.x - VEL > 0:  # LEFT
            TieFigther.x -= VEL
        if keys_pressed[pygame.K_d] and TieFigther.x + VEL + TieFigther.width < BORDER.x:  # RIGHT
            TieFigther.x += VEL
        if keys_pressed[pygame.K_w] and TieFigther.y - VEL > 0:  # UP
            TieFigther.y -= VEL
        if keys_pressed[pygame.K_s] and TieFigther.y + VEL + TieFigther.height < HEIGHT - 15:  # DOWN
            TieFigther.y += VEL