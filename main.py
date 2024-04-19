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
LEVEL_DURATION = 10000  # 30 seconds in milliseconds
level_time_passed = 0

# Fonts
font = pygame.font.Font("assets/fonts/ka1.TTF", 60)
font_small = pygame.font.Font("assets/fonts/ka1.ttf", 20)
game_over = font.render("Game Over", True, BLACK)

# Load images
background = pygame.image.load("assets/images/pf-background.png")

DISPLAYSURF = pygame.display.set_mode((400, 600))
pygame.display.set_caption("Game")


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.randomPos = random.randint(40, SCREEN_WIDTH - 40)
        self.image = pygame.image.load(f"assets/images/enemy{random.randint(1, 3)}.png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = pygame.rect.Rect(self.randomPos, 0, 50, 50)
        self.rect.center = (self.randomPos, 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.top > 600:
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/images/player.png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = pygame.rect.Rect(160, 620, 50, 50)
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.top:
            if pressed_keys[K_UP]:
                self.image = pygame.image.load("assets/images/player2.png")
                self.image = pygame.transform.scale(self.image, (100, 100))
                self.rect.move_ip(0, -5)
        if self.rect.bottom:
            if pressed_keys[K_DOWN]:
                self.image = pygame.image.load("assets/images/player.png")
                self.image = pygame.transform.scale(self.image, (100, 100))
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


class Cup(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/images/cup.png")
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > 600:
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


class Win(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/images/sandwich.png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (200, 20)

    def move(self):
        self.rect.move_ip(0, 0)
        if self.rect.top > 600:
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


# Setting up Sprites
P1 = Player()
E1 = Enemy()
C1 = Cup()
W1 = Win()
# Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
coins.add(C1)
win = pygame.sprite.Group()
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
        if event.type == INC_SPEED:
            SPEED += 0.5
        if event.type == QUIT:
            pygame.quit()
            # sys.exit()
    print(level_time_passed)

    if level_time_passed >= LEVEL_DURATION:
        start_time = current_time  # Reset timer for the next level
        LEVEL += 1
        if LEVEL == 2:
            background = pygame.image.load("assets/images/ab-background.png")
        if LEVEL == 3:
            background = pygame.image.load("assets/images/kb-background.png")

        # continue
    if LEVEL > 3:
        for enemy in enemies:
            enemy.kill()
        for enemy in coins:
            enemy.kill()
        win.add(W1)
        all_sprites.add(W1)
        if P1.collect_coin(win):
            DISPLAYSURF.fill(GREEN)
            DISPLAYSURF.blit(game_over, (30, 250))
            pygame.display.update()
            time.sleep(2)
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(background, (0, 0))
    coin_scores = font_small.render(str(COIN_SCORE), True, BLACK)
    lives = font_small.render(str(LIVES), True, RED)
    level_score = font_small.render(f"Level - {LEVEL}", True, BLACK)
    DISPLAYSURF.blit(level_score, (10, 10))
    # DISPLAYSURF.blit(coin_scores, (360, 10))
    DISPLAYSURF.blit(lives, (360, 10))

    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    if P1.collect_coin(coins):
        pygame.mixer.Sound('assets/audio/catch.mp3').play()
        COIN_SCORE += 1
        TOTAL_SCORE += random.randint(0, 10)
        new_coin = Cup()
        coins.add(new_coin)
        all_sprites.add(new_coin)
    for enemy in list(enemies):  # Iterate over a copy of the list to avoid modification issues during iteration
        if pygame.sprite.collide_rect(P1, enemy):
            print(f"Collision with enemy at {enemy.rect}")  # Debug print
            enemy.kill()  # This should only kill the collided enemy
            LIVES -= 1
            P1.rect.left = 200
            time.sleep(0.2)
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
            break  # Ensure we only handle one collision and then exit the loop

    if LIVES == 0:
        # pygame.mixer.Sound('assets/crash.wav').play()
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
