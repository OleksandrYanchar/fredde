import pygame
import random
import sys

pygame.init()

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
ENEMY_WIDTH = 40
ENEMY_HEIGHT = 40
ENEMY_SPEED = 5

SCORE_INCREMENT = 10
MAX_LIVES = 3
ENEMY_SPAWN_TIME = 1000
BEST_SCORE_FILE = "best_score.txt"

def game_over_screen(window, score, best_score):
    window.fill(BLACK)
    draw_text(window, "Game Over!", 48, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 100, WHITE)
    draw_text(window, f"Your Score: {score} points", 36, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50, WHITE)
    draw_text(window, f"Best Score: {best_score} points", 36, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, WHITE)
    draw_text(window, "Press 'R' to Restart", 24, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50, WHITE)
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

def game_over():
    pygame.quit()
    sys.exit()

def draw_text(window, text, size, x, y, color):
    font = pygame.font.SysFont(None, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.centery = y
    window.blit(text_surface, text_rect)

def restart_game():
    global ENEMY_SPEED, score, lives, best_score
    ENEMY_SPEED = 5
    score = 0
    lives = MAX_LIVES
    best_score = load_best_score()

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

def game():
    global ENEMY_SPEED
    ENEMY_SPEED = 5

    window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption('Fredde the Enemy')
    clock = pygame.time.Clock()

    ENEMY_IMAGE = pygame.image.load('fredde.png')
    ENEMY_IMAGE = pygame.transform.scale(ENEMY_IMAGE, (ENEMY_WIDTH, ENEMY_HEIGHT))

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

        player_x = max(0, min(player_x, WINDOW_WIDTH - PLAYER_WIDTH))

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
        window.blit(ENEMY_IMAGE, (enemy_x, enemy_y))
        draw_text(window, f"Score: {score}", 24, 70, 30, WHITE)
        draw_text(window, f"Lives: {lives}", 24, 730, 30, WHITE)
        draw_text(window, f"Best Score: {best_score}", 24, WINDOW_WIDTH // 2, 30, WHITE)

        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    restart_game()
    game()
