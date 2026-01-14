import pygame
 
pygame.init()
 
print_message = pygame.USEREVENT + 0
DOGE = pygame.USEREVENT + 1
pygame.time.set_timer(print_message, 3000)

def yellow_handle_movement(keys_pressed,speed, imortal):

    if keys_pressed[pygame.K_LSHIFT]:
        speed = 15
        imortal = False
        pygame.event.post(pygame.event.Event(DOGE))
        print(speed,"  ",imortal)
        pygame.time.set_timer(DOGE, 3000)
 
while True:
    imortal = True
    speed = 5
    for event in pygame.event.get():
        if event.type == print_message:
            print("Hello World")
            print(speed,imortal)

    keys_pressed = pygame.key.get_pressed()
    yellow_handle_movement(keys_pressed, speed, imortal)