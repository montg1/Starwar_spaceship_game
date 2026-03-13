import pygame
import os
from Network import Network

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1080, 720
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (0, 255, 0)

BORDER = pygame.Rect(WIDTH // 2 - 5, 10, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Grenade+1.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/Gun+Silencer.mp3')

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
INFO_FONT = pygame.font.SysFont('comicsans', 60)

FPS = 60
SPEED = 5
BULLET_SPEED = 10
MAX_BULLETS = 4
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 75, 75
TIE_FIGHTER_WIDTH, TIE_FIGHTER_HEIGHT = 55, 75

TIE_FIGHTER_HIT = pygame.USEREVENT + 1
X_WING_HIT = pygame.USEREVENT + 2

TIE_FIGHTER_IMAGE = pygame.image.load(os.path.join('starwarship', 'Tie-Fighter.png'))
TIE_FIGHTER = pygame.transform.rotate(
    pygame.transform.scale(TIE_FIGHTER_IMAGE, (TIE_FIGHTER_WIDTH, TIE_FIGHTER_HEIGHT)), 90)

X_WING_IMAGE = pygame.image.load(os.path.join('starwarship', 'X_Wing.png'))
X_WING = pygame.transform.rotate(
    pygame.transform.scale(X_WING_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(
    pygame.image.load(os.path.join('starwarship', 'space.gif')), (WIDTH, HEIGHT))

SHIELD_IMAGE = pygame.image.load(os.path.join("starwarship", "ShieldHit.png"))
SHIELD = pygame.transform.rotate(
    pygame.transform.scale(SHIELD_IMAGE, (120, 120)), 0)


def draw_window(tie_rect, xwing_rect, tie_bullets, xwing_bullets,
                tie_health, xwing_health, shield_tie, shield_xwing):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    # Health text
    xwing_health_text = HEALTH_FONT.render("Energy Shield: " + str(xwing_health), 1, WHITE)
    tie_health_text = HEALTH_FONT.render("Energy Shield: " + str(tie_health), 1, WHITE)
    WIN.blit(xwing_health_text, (WIDTH - xwing_health_text.get_width() - 10, 10))
    WIN.blit(tie_health_text, (10, 10))

    # Ships
    WIN.blit(TIE_FIGHTER, (tie_rect.x, tie_rect.y))
    WIN.blit(X_WING, (xwing_rect.x, xwing_rect.y))

    # Shields (only if health > 0)
    if tie_health > 0:
        WIN.blit(SHIELD, (shield_tie.x, shield_tie.y))
    if xwing_health > 0:
        WIN.blit(SHIELD, (shield_xwing.x, shield_xwing.y))

    # Bullets
    for bullet in tie_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    for bullet in xwing_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    pygame.display.update()


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH / 2 - draw_text.get_width() / 2,
                         HEIGHT / 2 - draw_text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(3000)


def draw_waiting():
    WIN.blit(SPACE, (0, 0))
    text = INFO_FONT.render("Waiting for opponent...", 1, WHITE)
    WIN.blit(text, (WIDTH / 2 - text.get_width() / 2,
                    HEIGHT / 2 - text.get_height() / 2))
    pygame.display.update()


def main():
    # Connect to server
    net = Network()
    player_id = net.get_player_id()

    if player_id is None:
        print("Could not connect to server!")
        print("Make sure the server is running: python3 sever.py")
        return

    if player_id == 0:
        pygame.display.set_caption("Player 1: Tie Fighter (WASD + LCtrl)")
    else:
        pygame.display.set_caption("Player 2: X-Wing (Arrows + RCtrl)")

    print(f"Connected as Player {player_id + 1}")

    # Show waiting screen until both players connect
    draw_waiting()
    print("Waiting for opponent to connect...")
    ready = net.wait_for_ready()
    if not ready:
        print("Failed to get ready signal from server!")
        return
    print("Both players connected! Game starting!")

    # Initial positions
    tie_rect = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    xwing_rect = pygame.Rect(900, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    shield_tie = pygame.Rect(90, 268, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    shield_xwing = pygame.Rect(890, 277, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    tie_bullets = []
    xwing_bullets = []

    tie_health = 4
    xwing_health = 4

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                # Player 0 (Tie Fighter) shoots with LCtrl
                if player_id == 0 and event.key == pygame.K_LCTRL and len(tie_bullets) < MAX_BULLETS:
                    offset = 10 if len(tie_bullets) % 2 == 0 else 20
                    bullet = pygame.Rect(
                        tie_rect.x + tie_rect.width,
                        tie_rect.y + tie_rect.height // 2 - offset, 10, 5)
                    tie_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                # Player 1 (X-Wing) shoots with RCtrl
                if player_id == 1 and event.key == pygame.K_RCTRL and len(xwing_bullets) < MAX_BULLETS:
                    offset = 30 if len(xwing_bullets) % 2 == 0 else -30
                    bullet = pygame.Rect(
                        xwing_rect.x,
                        xwing_rect.y + xwing_rect.height // 2 - offset, 10, 5)
                    xwing_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

        # Movement - only control your own ship
        keys = pygame.key.get_pressed()

        if player_id == 0:
            # Tie Fighter movement (WASD)
            if keys[pygame.K_a] and tie_rect.x - SPEED > 0 and tie_rect.x >= 20:
                tie_rect.x -= SPEED
                shield_tie.x -= SPEED
            if keys[pygame.K_d] and tie_rect.x + SPEED + tie_rect.width < BORDER.x:
                tie_rect.x += SPEED
                shield_tie.x += SPEED
            if keys[pygame.K_w] and tie_rect.y - SPEED > 0 and tie_rect.y >= 60:
                tie_rect.y -= SPEED
                shield_tie.y -= SPEED
            if keys[pygame.K_s] and tie_rect.y + SPEED + tie_rect.height < HEIGHT - 15:
                tie_rect.y += SPEED
                shield_tie.y += SPEED

            # Move Tie bullets
            for bullet in tie_bullets[:]:
                bullet.x += BULLET_SPEED
                if xwing_rect.colliderect(bullet):
                    xwing_health -= 1
                    tie_bullets.remove(bullet)
                    BULLET_HIT_SOUND.play()
                elif bullet.x > WIDTH:
                    tie_bullets.remove(bullet)

        elif player_id == 1:
            # X-Wing movement (Arrow keys)
            if keys[pygame.K_LEFT] and xwing_rect.x >= 565 and xwing_rect.x - SPEED > BORDER.x + BORDER.width:
                xwing_rect.x -= SPEED
                shield_xwing.x -= SPEED
            if keys[pygame.K_RIGHT] and xwing_rect.x + SPEED + xwing_rect.width < WIDTH and xwing_rect.x <= 980:
                xwing_rect.x += SPEED
                shield_xwing.x += SPEED
            if keys[pygame.K_UP] and xwing_rect.y - SPEED > 0 and xwing_rect.y >= 45:
                xwing_rect.y -= SPEED
                shield_xwing.y -= SPEED
            if keys[pygame.K_DOWN] and xwing_rect.y + SPEED + xwing_rect.height < HEIGHT - 15:
                xwing_rect.y += SPEED
                shield_xwing.y += SPEED

            # Move X-Wing bullets
            for bullet in xwing_bullets[:]:
                bullet.x -= BULLET_SPEED
                if tie_rect.colliderect(bullet):
                    tie_health -= 1
                    xwing_bullets.remove(bullet)
                    BULLET_HIT_SOUND.play()
                elif bullet.x < 0:
                    xwing_bullets.remove(bullet)

        # Prepare our state to send
        if player_id == 0:
            my_state = {
                "pos": (tie_rect.x, tie_rect.y),
                "shield_pos": (shield_tie.x, shield_tie.y),
                "bullets": [(b.x, b.y, b.width, b.height) for b in tie_bullets],
                "health": tie_health,
                "opponent_health": xwing_health,
            }
        else:
            my_state = {
                "pos": (xwing_rect.x, xwing_rect.y),
                "shield_pos": (shield_xwing.x, shield_xwing.y),
                "bullets": [(b.x, b.y, b.width, b.height) for b in xwing_bullets],
                "health": xwing_health,
                "opponent_health": tie_health,
            }

        # Send state and get opponent state
        opponent = net.send(my_state)

        if opponent is not None:
            # Update opponent's data
            if player_id == 0:
                # We are Tie, opponent is X-Wing
                xwing_rect.x, xwing_rect.y = opponent["pos"]
                shield_xwing.x, shield_xwing.y = opponent["shield_pos"]
                xwing_bullets = [pygame.Rect(b[0], b[1], b[2], b[3]) for b in opponent["bullets"]]
                xwing_health = opponent["health"]
                tie_health = opponent.get("opponent_health", tie_health)
            else:
                # We are X-Wing, opponent is Tie
                tie_rect.x, tie_rect.y = opponent["pos"]
                shield_tie.x, shield_tie.y = opponent["shield_pos"]
                tie_bullets = [pygame.Rect(b[0], b[1], b[2], b[3]) for b in opponent["bullets"]]
                tie_health = opponent["health"]
                xwing_health = opponent.get("opponent_health", xwing_health)

        # Check winner
        winner_text = ""
        if xwing_health < 0:
            winner_text = "Tie Fighter Wins!"
        if tie_health < 0:
            winner_text = "X-Wing Wins!"

        if winner_text:
            draw_winner(winner_text)
            break

        draw_window(tie_rect, xwing_rect, tie_bullets, xwing_bullets,
                    tie_health, xwing_health, shield_tie, shield_xwing)

    pygame.quit()


if __name__ == "__main__":
    main()
