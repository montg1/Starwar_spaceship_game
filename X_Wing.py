import pygame
import os

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 75, 75
VEL = 5
BULLET_VEL = 10
MAX_BULLETS = 40

X_Wing_Image = pygame.image.load(
    os.path.join('starwarship', 'X_Wing.png'))
X_Wing_ship = pygame.transform.rotate(pygame.transform.scale(
    X_Wing_Image, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

def X_Wing_Movement(keys_pressed, X_Wing, BORDER, HEIGHT):
    if keys_pressed[pygame.K_LEFT] and X_Wing.x - VEL > 0:  # LEFT
        X_Wing.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and X_Wing.x + VEL + X_Wing.width < BORDER.x:  # RIGHT
        X_Wing.x += VEL
    if keys_pressed[pygame.K_UP] and X_Wing.y - VEL > 0:  # UP
        X_Wing.y -= VEL
    if keys_pressed[pygame.K_DOWN] and X_Wing.y + VEL + X_Wing.height < HEIGHT - 15:  # DOWN
        X_Wing.y += VEL