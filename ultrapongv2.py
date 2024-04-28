import pygame
import sys
import random
from array import array

# Initialize Pygame and its mixer
pygame.init()
pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)

# Screen and game settings
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
FPS = 60
CLOCK = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Paddle and ball settings
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 15
PLAYER_SPEED = 7
BALL_SPEED_X, BALL_SPEED_Y = 7, 7

# Positions
player1_pos = [30, (SCREEN_HEIGHT - PADDLE_HEIGHT) // 2]
player2_pos = [SCREEN_WIDTH - 30 - PADDLE_WIDTH, (SCREEN_HEIGHT - PADDLE_HEIGHT) // 2]
ball_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]

# Score
player1_score = 0
player2_score = 0

# Sound synthesis function
def generate_beep_sound(frequency=440, duration=0.1):
    sample_rate = pygame.mixer.get_init()[0]
    max_amplitude = 2 ** (abs(pygame.mixer.get_init()[1]) - 1) - 1
    samples = int(sample_rate * duration)
    wave = [int(max_amplitude * ((i // (sample_rate // frequency)) % 2)) for i in range(samples)]
    sound = pygame.mixer.Sound(buffer=array('h', wave))
    sound.set_volume(0.1)
    return sound

# Sound effects
hit_sound = generate_beep_sound(660, 0.05)
score_sound = generate_beep_sound(330, 0.3)

def move_ball():
    global ball_pos, BALL_SPEED_X, BALL_SPEED_Y, player1_score, player2_score

    # Move the ball
    ball_pos[0] += BALL_SPEED_X
    ball_pos[1] += BALL_SPEED_Y

    # Collide with top and bottom
    if ball_pos[1] <= 0 or ball_pos[1] >= SCREEN_HEIGHT - BALL_SIZE:
        BALL_SPEED_Y *= -1

    # Collide with paddles
    if (ball_pos[0] <= player1_pos[0] + PADDLE_WIDTH and
        player1_pos[1] < ball_pos[1] < player1_pos[1] + PADDLE_HEIGHT) or \
       (ball_pos[0] + BALL_SIZE >= player2_pos[0] and
        player2_pos[1] < ball_pos[1] < player2_pos[1] + PADDLE_HEIGHT):
        BALL_SPEED_X *= -1
        hit_sound.play()

    # Scoring
    if ball_pos[0] < 0:
        player2_score += 1
        score_sound.play()
        reset_ball()
    elif ball_pos[0] > SCREEN_WIDTH:
        player1_score += 1
        score_sound.play()
        reset_ball()

def reset_ball():
    global ball_pos, BALL_SPEED_X
    ball_pos = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
    BALL_SPEED_X *= -1  # Change direction

def draw_elements():
    SCREEN.fill(BLACK)
    # Draw paddles
    pygame.draw.rect(SCREEN, WHITE, pygame.Rect(player1_pos[0], player1_pos[1], PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(SCREEN, WHITE, pygame.Rect(player2_pos[0], player2_pos[1], PADDLE_WIDTH, PADDLE_HEIGHT))
    # Draw ball
    pygame.draw.ellipse(SCREEN, WHITE, pygame.Rect(ball_pos[0], ball_pos[1], BALL_SIZE, BALL_SIZE))
    # Score display
    font = pygame.font.Font(None, 74)
    score_text = font.render(f"{player1_score} : {player2_score}", True, WHITE)
    SCREEN.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 10))

def main():
    global player1_pos, player2_pos

    while True:
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and player1_pos[1] > 0:
            player1_pos[1] -= PLAYER_SPEED
        if keys[pygame.K_s] and player1_pos[1] < SCREEN_HEIGHT - PADDLE_HEIGHT:
            player1_pos[1] += PLAYER_SPEED
        if keys[pygame.K_UP] and player2_pos[1] > 0:
            player2_pos[1] -= PLAYER_SPEED
        if keys[pygame.K_DOWN] and player2_pos[1] < SCREEN_HEIGHT - PADDLE_HEIGHT:
            player2_pos[1] += PLAYER_SPEED

        move_ball()
        draw_elements()
        pygame.display.update()

if __name__ == "__main__":
    main()
