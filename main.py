import random
import time
import pygame
import sys
from pygame.locals import *

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

# Colors and dimensions
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIVES = 3
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COIN_SCORE = 0
TOTAL_SCORE = 0
LEVEL = 1
LEVEL_DURATION = 5000  # 30 seconds in milliseconds
level_time_passed = 0

# Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Load images
background = pygame.image.load("assets/AnimatedStreet.png")

DISPLAYSURF = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Game")


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.top > 600:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.top:
            if pressed_keys[K_UP]:
                self.rect.move_ip(0, -5)
        if self.rect.bottom:
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0, 5)

        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

    def collect_coin(self, coins):
        collisions = pygame.sprite.spritecollide(self, coins, True)
        for coin in collisions:
            return True
        return False


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/coin.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > 600:
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


# Setting up Sprites
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
coins.add(C1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

# Adding a new User event
INC_SPEED = pygame.USEREVENT
pygame.time.set_timer(INC_SPEED, 1000)

# Game Loop
start_time = pygame.time.get_ticks()  # Start the timer for level duration
while True:
    current_time = pygame.time.get_ticks()
    level_time_passed = current_time - start_time

    # Cycles through all events occurring
    for event in pygame.event.get():
        # if event.type == INC_SPEED:
        #     SPEED += 0.5
        if event.type == QUIT:
            pygame.quit()
            # sys.exit()
    print(level_time_passed)

    if level_time_passed >= 3000:
        start_time = current_time  # Reset timer for the next level
        LEVEL += 1
        # continue
    if LEVEL > 3:
        # print("end")
        time.sleep(0.5)

        DISPLAYSURF.fill(GREEN)
        DISPLAYSURF.blit(game_over, (30, 250))

        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    DISPLAYSURF.blit(background, (0, 0))
    scores = font_small.render(str(SCORE), True, BLACK)
    coin_scores = font_small.render(str(COIN_SCORE), True, BLACK)
    total_scores = font_small.render(str(TOTAL_SCORE), True, BLACK)
    lives = font_small.render(str(LIVES), True, RED)
    level_score = font_small.render(str(LEVEL), True, BLACK)
    DISPLAYSURF.blit(level_score, (10, 10))
    DISPLAYSURF.blit(coin_scores, (360, 10))
    DISPLAYSURF.blit(total_scores, (360, 30))
    DISPLAYSURF.blit(total_scores, (360, 30))
    DISPLAYSURF.blit(lives, (200, 30))

    # Moves and Re-draws all Sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    if P1.collect_coin(coins):
        COIN_SCORE += 1
        TOTAL_SCORE += random.randint(0, 10)
        new_coin = Coin()
        coins.add(new_coin)
        all_sprites.add(new_coin)
    collided_enemies = pygame.sprite.spritecollide(P1, enemies,
                                                   True)  # True will remove the sprite from 'enemies' group
    if collided_enemies:
        LIVES -= 1  # Reduce lives if there is a collision
        P1.rect.left = 200  # Reset the player's position
        time.sleep(0.2)  # Brief pause to indicate collision

    if LIVES == 0:
        pygame.mixer.Sound('assets/crash.wav').play()
        time.sleep(0.5)

        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))

        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)
