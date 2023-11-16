import pygame
import sys
import time
import random
import threading
import re
from pygame.locals import *
from player import Player
from enemy1 import Enemy1
from enemy2 import Enemy2
from enemy3 import Enemy3
from background import Background
from score_manager import ScoreManager


pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()


RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SCORE = 0


font = pygame.font.SysFont("malgungothic", 60)
font_small = pygame.font.SysFont("malgungothic", 20)
game_over = font.render("KONIEC GRY", True, BLACK)


DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")


P1 = Player()

background = Background()


enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)

enemy_spawn_timer = pygame.time.get_ticks()
enemy_spawn_delay = 2000  # delay between enemy spawns

score_manager = ScoreManager()
score_manager.load_scores()

entering_nickname = False

# Funkcja do odtwarzania muzyki w tle na osobnym wątku
def play_background_music():
    pygame.mixer.music.load("japanese-jazz.mp3")
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)


# Uruchomienie wątku z muzyką w tle
music_thread = threading.Thread(target=play_background_music)
music_thread.start()



def is_valid_nickname(nickname):
    pattern = r"^[a-z]+$"  # Tylko małe litery
    return re.match(pattern, nickname) is not None



def display_enter_nickname_screen():
    entering_nickname = True
    nickname_input = ""

    while entering_nickname:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    nickname_input = nickname_input[:-1]
                elif event.key == K_RETURN:
                    if is_valid_nickname(nickname_input) and SCORE > 0:
                        score_manager.save_score(nickname_input, SCORE)
                        entering_nickname = False
                elif event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)
                else:
                    char = event.unicode
                    if len(nickname_input) < 8 and char.islower():
                        nickname_input += char

        DISPLAYSURF.fill(WHITE)
        nickname_text = font_small.render("Wpisz nick (tylko małe litery):", True, BLACK)
        nickname_text_rect = nickname_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        DISPLAYSURF.blit(nickname_text, nickname_text_rect)

        nickname_input_text = font_small.render(nickname_input, True, BLACK)
        nickname_input_text_rect = nickname_input_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 25))
        DISPLAYSURF.blit(nickname_input_text, nickname_input_text_rect)

        pygame.display.update()
        FramePerSec.tick(FPS)


# game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit(0)

    current_time = pygame.time.get_ticks()

    if current_time - enemy_spawn_timer >= enemy_spawn_delay:
        enemy_spawn_timer = current_time

        # spawn new enemies
        if len(enemies) < 2:
            random_enemy_class = random.choice([Enemy1, Enemy2, Enemy3])
            new_enemy = random_enemy_class(SCORE)
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    background.update()

    DISPLAYSURF.fill(WHITE)
    background.render(DISPLAYSURF)

    scores2 = font_small.render(str(SCORE), True, BLACK)
    scores1 = font_small.render("wynik", True, BLACK)
    DISPLAYSURF.blit(scores1, (5, 5))
    DISPLAYSURF.blit(scores2, (5, 25))

    best_scorer = score_manager.scores.iloc[0]['Nickname']
    best_score = score_manager.scores.iloc[0]['Score']
    best_scorer_text = font_small.render(str(best_scorer), True, BLACK)
    best_score_text = font_small.render(str(best_score), True, BLACK)
    DISPLAYSURF.blit(best_scorer_text, (SCREEN_WIDTH - best_scorer_text.get_width() - 5, 5))
    DISPLAYSURF.blit(best_score_text, (SCREEN_WIDTH - best_score_text.get_width() - 5, 25))

    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()
        SCORE = sum(enemy.score for enemy in enemies)

    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound("jedziemy-dawaj-malina.wav").play()
        time.sleep(1)

        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))

        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)

        display_enter_nickname_screen()
        if not entering_nickname:
            P1 = Player()
            enemies = pygame.sprite.Group()
            all_sprites = pygame.sprite.Group()
            all_sprites.add(P1)
            SCORE = 0
            enemy_spawn_timer = pygame.time.get_ticks()

    pygame.display.update()
    FramePerSec.tick(FPS)
