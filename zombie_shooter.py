#T Tariq
#2024-01-09
#ZombieShooterFinalProject

#ENHANCEMENTS
'''
Include nice-looking graphics (png files are good for this) (0.5)
Use a custom pygame program icon (not the snake) (0.5)
Use lists to help make your program (0.5)
Use functions to help make your program (0.5)
Include sound (music / sfx) (1)
Use a timer (1)
'''
# Import necessary libraries
import pygame
import sys
import random
import os
from pygame import mixer

# Initialize Pygame and Pygame Mixer
pygame.init()
mixer.init()
mixer.music.load('song.mp3')

# Set program icon
programIcon = pygame.image.load('zombie.png')
pygame.display.set_icon(programIcon)

# Set up constants
WIDTH, HEIGHT = 800, 500
PLAYER_SPEED = 5
BULLET_SPEED = 7
ZOMBIE_SPEED = 2
ZOMBIE_SPAWN_DELAY = 60
WHITE = (255, 255, 255)
PLAYER_HEALTH = 50
ZOMBIE_HEALTH = 100
SCORE = 0
game_state = "start"
high_score_file = "high_score.txt"

# Frame variables for timer
frame_count = 0
frame_rate = 60
start_time = -1

# Set up Pygame screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie shooter game")

# Load images
background = pygame.image.load("background.webp")
background = pygame.transform.scale(background, [800, 500])
player_image = pygame.image.load("player.png")
player_image = pygame.transform.scale(player_image, [78, 123])
zombie_image = pygame.image.load("zombie.png")
zombie_image = pygame.transform.scale(zombie_image, [76, 124])

# Set up player rectangle
player = pygame.Rect(WIDTH//2 - 50, HEIGHT - 100, 100, 100)

# Lists for bullets and zombies
bullets = []
zombies = []

# Set up font and clock
font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

# Load high score
if os.path.exists(high_score_file):
    with open(high_score_file, 'r') as file:
        high_score = int(file.read())
else:
    high_score = 0

# Game loop
running = True
player_health = PLAYER_HEALTH

# Function for collision detection
def collisionDetection():
    global SCORE
    global player_health
    for bullet in bullets:
        for zombie in zombies:
            if bullet.colliderect(zombie):
                bullets.remove(bullet)
                zombies.remove(zombie)
                SCORE += 10

    for zombie in zombies:
        if zombie.colliderect(player):
            player_health -= 10
            zombies.remove(zombie)

# Play background music
mixer.music.play()

# Main game loop
while running:
    if game_state != "start":
        # Event handling during gameplay
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet = pygame.Rect(player.centerx-5, player.top, 10, 20)
                    bullets.append(bullet)

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            player.x += PLAYER_SPEED

        # Bullet movement and zombie spawning
        for bullet in bullets:
            bullet.y -= BULLET_SPEED
            if bullet.y < 0:
                bullets.remove(bullet)

        if random.randint(0, ZOMBIE_SPAWN_DELAY) == 0:
            zombie = pygame.Rect(random.randint(0, WIDTH-100), 0, 100, 10)
            zombies.append(zombie)

        # Zombie movement and collision detection
        for zombie in zombies:
            zombie.y += ZOMBIE_SPEED
            if zombie.y > HEIGHT:
                zombies.remove(zombie)

        collisionDetection()

        # Drawing on the screen
        screen.fill(WHITE)
        screen.blit(background, (0, 0))
        screen.blit(player_image, player)
        for zombie in zombies:
            screen.blit(zombie_image, zombie)
        for bullet in bullets:
            pygame.draw.rect(screen, (255, 0, 0), bullet)

        # Displaying game information
        total_seconds = frame_count // frame_rate
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        total_seconds += 1
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        frame_count += 1

        time_text = "Time played: {0:02}:{1:02}".format(minutes, seconds)
        time_text = font.render(time_text, True, WHITE)
        health_text = font.render(f"Health: {player_health}", True, (255, 0, 0))
        score_text = font.render(f"Score: {SCORE}", True, (0, 0, 255))
        high_score_text = font.render(f"High Score: {high_score}", True, (0, 255, 0))
        screen.blit(health_text, (10, 10))
        screen.blit(score_text, (10, 50))
        screen.blit(time_text, (10, 90))
        screen.blit(high_score_text, (WIDTH - 200, 10))

        # Check for game over
        if player_health <= 0:
            if SCORE > high_score:
                high_score = SCORE
                with open(high_score_file, 'w') as file:
                    file.write(str(high_score))
            running = False

        pygame.display.flip()
        clock.tick(60)
    else:
        # Event handling during start screen
        screen.blit(background, (0, 0))
        starting_text = "Zombie Shooter"
        starting_text2 = "CLICK TO PLAY!"
        controls_text_line1 = "Controls: Left/Right Arrow keys to move"
        controls_text_line2 = "SPACE to shoot"
        high_score_text = f"High Score: {high_score}"  # Update with actual high score logic

        # Render text with neon green color
        starting_text = font.render(starting_text, True, (0, 255, 0))
        starting_text2 = font.render(starting_text2, True, (0, 255, 0))
        controls_text_line1 = font.render(controls_text_line1, True, (0, 255, 0))
        controls_text_line2 = font.render(controls_text_line2, True, (0, 255, 0))
        high_score_text = font.render(high_score_text, True, (0, 255, 0))

        # Display text on the screen
        screen.blit(zombie_image, (192, 205))
        screen.blit(zombie_image, (492, 205))
        screen.blit(starting_text, (WIDTH//2-109, HEIGHT//2 - 60))
        screen.blit(controls_text_line1, (WIDTH//2-180, HEIGHT//2))
        screen.blit(controls_text_line2, (WIDTH//2-110, HEIGHT//2 + 30))
        screen.blit(starting_text2, (WIDTH//2-109, HEIGHT//2 + 70))
        screen.blit(high_score_text, (WIDTH//2-100, HEIGHT//2 + 110))

        # Event handling for starting the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                game_state = "playing"

        pygame.display.flip()

# Game over screen
if game_state != "start":
    game_over_text = font.render(f"Game OVER ! Score: {SCORE}", True, (0, 255, 0))
    screen.blit(game_over_text, (WIDTH//2-137, HEIGHT//2 - 20))
    pygame.display.flip()

# Delay before quitting
pygame.time.delay(1000)
pygame.quit()
sys.exit()




