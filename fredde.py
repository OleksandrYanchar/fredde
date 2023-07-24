import pygame
import random
import sys

pygame.init()

# Constants for the game window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

# Constants for colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Constants for game objects
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
ENEMY_WIDTH = 40
ENEMY_HEIGHT = 40
ENEMY_SPEED = 5

# Constants for the game
SCORE_INCREMENT = 10
MAX_LIVES = 3
ENEMY_SPAWN_TIME = 1000  # milliseconds
BEST_SCORE_FILE = "best_score.txt"

# Function to end the game and show results
def game_over_screen(window, score, best_score):
    window.fill(BLACK)
    draw_text(window, "Game Over!", 48, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50, WHITE)
    draw_text(window, f"Your Score: {score} points", 36, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, WHITE)
    draw_text(window, f"Best Score: {best_score} points", 36, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50, WHITE)
    draw_text(window, "Press 'R' to Restart", 24, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 100, WHITE)
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    restart_game()
                    game()

# Function to end the game
def game_over():
    pygame.quit()
    sys.exit()

# Function to display text on the screen
def draw_text(window, text, size, x, y, color):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.centery = y
    window.blit(text_surface, text_rect)

# Function to restart the game
def restart_game():
    global ENEMY_SPEED, score, lives
    ENEMY_SPEED = 5
    score = 0
    lives = MAX_LIVES

def load_best_score():
    try:
        with open(BEST_SCORE_FILE, "r") as file:
            content = file.read().strip()
            if content.isdigit():
                best_score = int(content)
                return best_score
            else:
                return 0
    except FileNotFoundError:
        return 0

def save_best_score(best_score):
    with open(BEST_SCORE_FILE, "w") as file:
        file.write(str(best_score))

# Flappy Bird mini-game
def flappy_bird_game(window):
    BIRD_WIDTH = 50
    BIRD_HEIGHT = 50
    BIRD_GRAVITY = 0.3
    BIRD_FLAP_FORCE = -7
    bird_x = WINDOW_WIDTH // 3
    bird_y = WINDOW_HEIGHT // 2
    bird_velocity = 0

    # Load the bird image and resize it to match the bird's dimensions
    BIRD_IMAGE = pygame.image.load('bird.png')
    BIRD_IMAGE = pygame.transform.scale(BIRD_IMAGE, (BIRD_WIDTH, BIRD_HEIGHT))

    # List to store the pipes
    pipes = []

    # Timer for spawning pipes
    pipe_spawn_timer = pygame.time.get_ticks()

    # Game loop for Flappy Bird
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_velocity += BIRD_FLAP_FORCE

        bird_velocity += BIRD_GRAVITY
        bird_y += bird_velocity

        if bird_y < 0:
            bird_y = 0
            bird_velocity = 0
        elif bird_y + BIRD_HEIGHT > WINDOW_HEIGHT:
            bird_y = WINDOW_HEIGHT - BIRD_HEIGHT
            bird_velocity = 0

        # Update pipes positions
        for pipe in pipes:
            pipe['x'] -= ENEMY_SPEED

        # Remove off-screen pipes
        pipes = [pipe for pipe in pipes if pipe['x'] + ENEMY_WIDTH > 0]

        # Spawn new pipes every ENEMY_SPAWN_TIME milliseconds
        current_time = pygame.time.get_ticks()
        if current_time - pipe_spawn_timer > ENEMY_SPAWN_TIME:
            pipe_height = random.randint(100, WINDOW_HEIGHT - 200)
            pipes.append({'x': WINDOW_WIDTH, 'y': 0, 'height': pipe_height, 'counted': False})
            pipes.append({'x': WINDOW_WIDTH, 'y': pipe_height + 200, 'height': WINDOW_HEIGHT, 'counted': False})
            pipe_spawn_timer = current_time

        # Check for collisions with pipes
        for pipe in pipes:
            if bird_x + BIRD_WIDTH > pipe['x'] and bird_x < pipe['x'] + ENEMY_WIDTH:
                if bird_y < pipe['height'] or bird_y + BIRD_HEIGHT > pipe['y']:
                    # Collision with a pipe, game over
                    collision_sound.play()
                    game_over_screen(window, score, best_score)

        # Check if bird passes through a pipe for scoring
        for pipe in pipes:
            if pipe['x'] + ENEMY_WIDTH < bird_x and not pipe['counted']:
                score += 1
                pipe['counted'] = True
                score_sound.play()

        window.fill(BLACK)
        draw_bird(window, bird_x, bird_y)  # Use a custom function to draw the bird

        # Draw pipes
        for pipe in pipes:
            pygame.draw.rect(window, WHITE, (pipe['x'], pipe['y'], ENEMY_WIDTH, pipe['height']))
            pygame.draw.rect(window, WHITE, (pipe['x'], pipe['y'] + pipe['height'] + 200, ENEMY_WIDTH, WINDOW_HEIGHT))

        draw_text(window, f"Score: {score}", 24, 70, 30, WHITE)
        draw_text(window, f"Lives: {lives}", 24, 730, 30, WHITE)
        draw_text(window, f"Best Score: {best_score}", 24, WINDOW_WIDTH // 2, 30, WHITE)

        pygame.display.update()
        clock.tick(FPS)

# Flappy Fredde mini-game
def flappy_fredde_game(window):
    FREDDE_WIDTH = 50
    FREDDE_HEIGHT = 50
    FREDDE_GRAVITY = 0.3
    FREDDE_FLAP_FORCE = -7
    fredde_x = WINDOW_WIDTH // 3
    fredde_y = WINDOW_HEIGHT // 2
    fredde_velocity = 0

    # Load the Flappy Fredde image and resize it to match its dimensions
    FREDDE_IMAGE = pygame.image.load('fredde.png')
    FREDDE_IMAGE = pygame.transform.scale(FREDDE_IMAGE, (FREDDE_WIDTH, FREDDE_HEIGHT))

    # List to store the pipes
    pipes = []

    # Timer for spawning pipes
    pipe_spawn_timer = pygame.time.get_ticks()

    # Game loop for Flappy Fredde
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    fredde_velocity += FREDDE_FLAP_FORCE

        fredde_velocity += FREDDE_GRAVITY
        fredde_y += fredde_velocity

        if fredde_y < 0:
            fredde_y = 0
            fredde_velocity = 0
        elif fredde_y + FREDDE_HEIGHT > WINDOW_HEIGHT:
            fredde_y = WINDOW_HEIGHT - FREDDE_HEIGHT
            fredde_velocity = 0

        # Update pipes positions
        for pipe in pipes:
            pipe['x'] -= ENEMY_SPEED

        # Remove off-screen pipes
        pipes = [pipe for pipe in pipes if pipe['x'] + ENEMY_WIDTH > 0]

        # Spawn new pipes every ENEMY_SPAWN_TIME milliseconds
        current_time = pygame.time.get_ticks()
        if current_time - pipe_spawn_timer > ENEMY_SPAWN_TIME:
            pipe_height = random.randint(100, WINDOW_HEIGHT - 200)
            pipes.append({'x': WINDOW_WIDTH, 'y': 0, 'height': pipe_height, 'counted': False})
            pipes.append({'x': WINDOW_WIDTH, 'y': pipe_height + 200, 'height': WINDOW_HEIGHT, 'counted': False})
            pipe_spawn_timer = current_time

        # Check for collisions with pipes
        for pipe in pipes:
            if fredde_x + FREDDE_WIDTH > pipe['x'] and fredde_x < pipe['x'] + ENEMY_WIDTH:
                if fredde_y < pipe['height'] or fredde_y + FREDDE_HEIGHT > pipe['y']:
                    # Collision with a pipe, game over
                    collision_sound.play()
                    game_over_screen(window, score, best_score)

        # Check if Flappy Fredde passes through a pipe for scoring
        for pipe in pipes:
            if pipe['x'] + ENEMY_WIDTH < fredde_x and not pipe['counted']:
                score += 1
                pipe['counted'] = True
                score_sound.play()

        window.fill(BLACK)
        draw_fredde(window, fredde_x, fredde_y)  # Use a custom function to draw Flappy Fredde

        # Draw pipes
        for pipe in pipes:
            pygame.draw.rect(window, WHITE, (pipe['x'], pipe['y'], ENEMY_WIDTH, pipe['height']))
            pygame.draw.rect(window, WHITE, (pipe['x'], pipe['y'] + pipe['height'] + 200, ENEMY_WIDTH, WINDOW_HEIGHT))

        draw_text(window, f"Score: {score}", 24, 70, 30, WHITE)
        draw_text(window, f"Lives: {lives}", 24, 730, 30, WHITE)
        draw_text(window, f"Best Score: {best_score}", 24, WINDOW_WIDTH // 2, 30, WHITE)

        pygame.display.update()
        clock.tick(FPS)

# Load the Fredde image and resize it to match the Fredde's dimensions
FREDDE_IMAGE = pygame.image.load('fredde.png')
FREDDE_IMAGE = pygame.transform.scale(FREDDE_IMAGE, (ENEMY_WIDTH, ENEMY_HEIGHT))

# Function to draw the bird
def draw_bird(window, x, y):
    window.blit(BIRD_IMAGE, (x, y))

# Function to draw Flappy Fredde
def draw_fredde(window, x, y):
    window.blit(FREDDE_IMAGE, (x, y))

# Main game function
def game():
    global ENEMY_SPEED
    ENEMY_SPEED = 5

    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Fredde the Enemy')
    clock = pygame.time.Clock()

    collision_sound = pygame.mixer.Sound('collision.wav')
    score_sound = pygame.mixer.Sound('score.wav')

    player_x = WINDOW_WIDTH // 2 - PLAYER_WIDTH // 2
    player_y = WINDOW_HEIGHT - PLAYER_HEIGHT
    enemy_x = random.randint(0, WINDOW_WIDTH - ENEMY_WIDTH)
    enemy_y = 0
    score = 0
    lives = MAX_LIVES
    best_score = load_best_score()
    last_enemy_spawn_time = pygame.time.get_ticks()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = True
                    while pause:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                game_over()
                            elif event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_p:
                                    pause = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_x -= 5
        if keys[pygame.K_RIGHT]:
            player_x += 5
        if keys[pygame.K_UP]:
            player_y -= 5
        if keys[pygame.K_DOWN]:
            player_y += 5

        player_x = max(0, min(player_x, WINDOW_WIDTH - PLAYER_WIDTH))
        player_y = max(0, min(player_y, WINDOW_HEIGHT - PLAYER_HEIGHT))

        if player_y <= 0:  # Player reached the upper boundary
            pygame.time.delay(500)  # Delay to display a transitional message
            draw_text(window, "Entering Flappy Fredde...", 36, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, WHITE)
            pygame.display.update()
            pygame.time.delay(1000)  # Delay before entering Flappy Fredde

            if score >= 1000:
                # Start Flappy Fredde game if score is 1000 or more
                score_in_flappy_fredde = flappy_fredde_game(window)
                score += score_in_flappy_fredde
                player_y = WINDOW_HEIGHT - PLAYER_HEIGHT

        enemy_y += ENEMY_SPEED

        if player_x < enemy_x + ENEMY_WIDTH and player_x + PLAYER_WIDTH > enemy_x and player_y < enemy_y + ENEMY_HEIGHT and player_y + PLAYER_HEIGHT > enemy_y:
            if lives <= 0:
                if score > best_score:
                    best_score = score
                    save_best_score(best_score)
                game_over_screen(window, score, best_score)
            else:
                collision_sound.play()
                lives -= 1
                enemy_x = random.randint(0, WINDOW_WIDTH - ENEMY_WIDTH)
                enemy_y = 0

        if enemy_y >= WINDOW_HEIGHT:
            score_sound.play()
            score += SCORE_INCREMENT
            enemy_x = random.randint(0, WINDOW_WIDTH - ENEMY_WIDTH)
            enemy_y = 0

        current_time = pygame.time.get_ticks()
        if current_time - last_enemy_spawn_time > ENEMY_SPAWN_TIME:
            ENEMY_SPEED += 1
            last_enemy_spawn_time = current_time

        window.fill(BLACK)
        pygame.draw.rect(window, WHITE, (player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT))
        window.blit(FREDDE_IMAGE, (enemy_x, enemy_y))
        draw_text(window, f"Score: {score}", 24, 70, 30, WHITE)
        draw_text(window, f"Lives: {lives}", 24, 730, 30, WHITE)
        draw_text(window, f"Best Score: {best_score}", 24, WINDOW_WIDTH // 2, 30, WHITE)

        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    restart_game()
    game()
