import random
import sys
import time

import pygame
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
font_biggest = pygame.font.Font("assets/fonts/ka1.TTF", 45)
font_big = pygame.font.Font("assets/fonts/ka1.ttf", 20)
font_medium = pygame.font.Font("assets/fonts/ka1.ttf", 10)
font_small = pygame.font.Font("assets/fonts/ka1.ttf", 5)
game_over = font_biggest.render("Game Over", True, BLACK)
Won = font_biggest.render("You Won!", True, BLACK)
# Load images
background = pygame.image.load("assets/images/pf-background.png")

DISPLAYSURF = pygame.display.set_mode((400, 600))


def show_intro_screen():
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE:  # Нажатие пробела начинает игру
                    intro = False

        DISPLAYSURF.fill((245, 245, 220))  # Задний фон
        intro_text = font_medium.render("Talgat has an EndTerm on statistics.", True, BLACK)
        intro_text2 = font_medium.render("He's very hungry!", True, BLACK)
        intro_text3 = font_medium.render("Help Talgat to run to Abylai Khan and buy a sandwich from Serik", True, BLACK)
        intro_text4 = font_medium.render("to make it to the EndTerm.", True, BLACK)
        start_text = font_big.render("Press Space to start", True, BLACK)
        DISPLAYSURF.blit(intro_text, (10, 100))  # Позиционирование текста
        DISPLAYSURF.blit(intro_text2, (10, 115))  # Позиционирование текста
        DISPLAYSURF.blit(intro_text3, (10, 130))  # Позиционирование текста
        DISPLAYSURF.blit(intro_text4, (10, 145))  # Позиционирование текста
        DISPLAYSURF.blit(start_text, (20, 400))
        pygame.display.update()
        FramePerSec.tick(FPS)


pygame.display.set_caption("Game")
show_intro_screen()


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.randomPos = random.randint(40, SCREEN_WIDTH - 40)
        # Список доступных изображений
        self.enemy_images = [
            pygame.image.load("assets/images/enemy1.png"),
            pygame.image.load("assets/images/enemy2.png"),
            pygame.image.load("assets/images/enemy3.png")
        ]
        # Выбор случайного изображения
        self.image = random.choice(self.enemy_images)
        self.image = pygame.transform.scale(self.image, (120, 120))
        self.rect = pygame.rect.Rect(self.randomPos, 0, 20, 60)
        self.rect.center = (self.randomPos, 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.top > 600:
            self.image = random.choice(self.enemy_images)
            self.image = pygame.transform.scale(self.image, (120,120))
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/images/player.png")
        self.image = pygame.transform.scale(self.image, (120,120))
        self.rect = pygame.rect.Rect(160, 620, 30, 50)
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.top:
            if pressed_keys[K_UP]:
                self.image = pygame.image.load("assets/images/player2.png")
                self.image = pygame.transform.scale(self.image, (120,120))
                self.rect.move_ip(0, -5)
        if self.rect.bottom:
            if pressed_keys[K_DOWN]:
                self.image = pygame.image.load("assets/images/player.png")
                self.image = pygame.transform.scale(self.image, (120,120))
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
            # self.rect.top = 0
            # self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
            self.kill()


class Win(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/images/sandwich.png")
        self.image = pygame.transform.scale(self.image, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (200, 100)

    def move(self):
        pass


class Health(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/images/heart3.png")
        self.image = pygame.transform.scale(self.image, (120, 70))
        self.rect = self.image.get_rect()
        self.rect.center = (360, 30)

    def changeState(self, lives_num):
        self.image = pygame.image.load(f"assets/images/heart{lives_num}.png")
        self.image = pygame.transform.scale(self.image, (120, 70))
        self.rect = self.image.get_rect()
        self.rect.center = (360, 30)

    def move(self):
        pass


def spawnCup():
    new_coin = Cup()
    coins.add(new_coin)
    all_sprites.add(new_coin)


# Setting up Sprites
P1 = Player()
E1 = Enemy()
C1 = Cup()
W1 = Win()
H1 = Health()
E2 = Enemy()
E3 = Enemy()
E4 = Enemy()
E5 = Enemy()
# Creating Sprites Groups
enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
coins.add(C1)
win = pygame.sprite.Group()
health = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)
all_sprites.add(H1)

# Adding a new User event
INC_SPEED = pygame.USEREVENT + 1
SPAWN_COIN = pygame.USEREVENT + 2
pygame.time.set_timer(INC_SPEED, 1000)
pygame.time.set_timer(SPAWN_COIN, 5000)

pygame.mixer.Sound('assets/audio/bg_sound.mp3').play(-1).set_volume(0.08)
# Game Loop
start_time = pygame.time.get_ticks()  # Start the timer for level duration
while True:
    current_time = pygame.time.get_ticks()
    level_time_passed = current_time - start_time

    # Cycles through all events occurring
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            SPEED += 0.2
        if event.type == SPAWN_COIN:
            spawnCup()
        if event.type == QUIT:
            pygame.quit()
            # sys.exit()

    if level_time_passed >= LEVEL_DURATION:
        start_time = current_time  # Reset timer for the next level
        LEVEL += 1
        if LEVEL == 2:
            time.sleep(0.5)
            DISPLAYSURF.fill(GREEN)
            DISPLAYSURF.blit(font_big.render("Kazybek Bi", True, BLACK), (30, 250))
            pygame.display.update()
            time.sleep(0.5)
            background = pygame.image.load("assets/images/kb-background.png")
            enemies.add(E2)
            all_sprites.add(E2)
            enemies.add(E3)
            all_sprites.add(E3)
            time.sleep(1)
        if LEVEL == 3:
            time.sleep(0.5)
            DISPLAYSURF.fill(RED)
            DISPLAYSURF.blit(font_big.render("Abylai Khan", True, BLACK), (30, 250))
            pygame.display.update()
            time.sleep(0.5)
            background = pygame.image.load("assets/images/ab-background.png")
            enemies.add(E4)
            all_sprites.add(E4)
            enemies.add(E5)
            all_sprites.add(E5)
            time.sleep(1)
            

        # continue
    if LEVEL > 3:
        for enemy in enemies:
            enemy.kill()
        for coin in coins:
            coin.kill()
        win.add(W1)
        all_sprites.add(W1)
        if P1.collect_coin(win):
            DISPLAYSURF.fill(GREEN)
            DISPLAYSURF.blit(Won, (70, 250))
            pygame.display.update()
            pygame.mixer.Sound('assets/audio/win.mp3').play()
            time.sleep(3.5)
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(background, (0, 0))
    coin_scores = font_big.render(str(COIN_SCORE), True, BLACK)
    level_score = font_big.render(f"Level - {LEVEL}", True, BLACK)
    if LEVEL > 3:
        epil = font_big.render("EPILOGUE", True, BLACK)
        DISPLAYSURF.blit(epil, (10, 10))
    else:
        DISPLAYSURF.blit(level_score, (10, 10))

    for entity in all_sprites:
        if entity != C1:
            DISPLAYSURF.blit(entity.image, entity.rect)
            entity.move()

    if P1.collect_coin(coins):
        pygame.mixer.Sound('assets/audio/catch.mp3').play()
        COIN_SCORE += 1
        TOTAL_SCORE += random.randint(0, 10)
        if LIVES != 3:
            LIVES += 1
            H1.changeState(LIVES)

    for enemy in list(enemies):  # Iterate over a copy of the list to avoid modification issues during iteration
        if pygame.sprite.collide_rect(P1, enemy):
            print(f"Collision with enemy at {enemy.rect}")  # Debug print
            pygame.mixer.Sound('assets/audio/punch.mp3').play().set_volume(0.2) #sound for collision
            enemy.kill()  # This should only kill the collided enemy
            LIVES -= 1
            if LIVES != 0:
                H1.changeState(LIVES)
            time.sleep(0.2)
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
            break  # Ensure we only handle one collision and then exit the loop
    if LIVES == 0:
        pygame.mixer.Sound('assets/audio/bg_sound.mp3')
        pygame.mixer.Sound('assets/audio/dead.mp3').play()
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
