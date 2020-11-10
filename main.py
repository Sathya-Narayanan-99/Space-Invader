import pygame
import math
import random
from pygame import mixer

# Inititialzing Pygame
pygame.init()

# Creating the screen
screen = pygame.display.set_mode((800, 600))

# Title and Icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load("Icon\spaceship.png").convert_alpha()
pygame.display.set_icon(icon)

# Background image
background = pygame.image.load("Images\Background.png").convert_alpha()
background = pygame.transform.scale(background, (800, 600))

# Background music
mixer.music.load(r"Sounds\background.wav")
mixer.music.play(-1)

# Player
playerImg = pygame.image.load("Images\player.png").convert_alpha()
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

# Multiple enemies
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load(r"Images\alien.png").convert_alpha())
    enemyX.append(random.randint(0, 800 - 64))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(1)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load("Images\laser.png").convert_alpha()
bulletX = random.randint(0, 800)
bulletY = 480
bulletX_change = 0
bulletY_change = 3.5
bullet_state = "Ready"  # Ready - bullet is invisible, Fire - bullet is visible

# Score
score_value = 0
font = pygame.font.FontType(r'Font\freesansbold.ttf', 32)
prev_score_value = 0.1
speed_multiplier = 1
textX = 10
textY = 10

# Game over
gameover_font = pygame.font.FontType(r'Font\freesansbold.ttf', 64)


# Score display function
def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


# Game over function
def game_over_text():
    game_over = gameover_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(game_over, (200, 200))
    restart = font.render("Press 'R' to Replay ", True, (255, 255, 255))
    quit = font.render("Press 'X' to Quit", True, (255, 255, 255))
    screen.blit(restart, (250, 280))
    screen.blit(quit, (250, 330))  # y=330 if replay is working


# Player spawn function
def player(x, y):
    screen.blit(playerImg, (x, y))


# Enemy spawn function
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# Bullet spawn function
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "Fire"
    screen.blit(bulletImg, (x + 16, y + 10))  # Value is added so that the bullet appears on the centre


# To find a collison occurance between enemy and bullet
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 30:
        return True
    return False


# Game Loop
running = True
while running:
    # RGB
    screen.fill((0, 0, 0))

    # Displaying background image
    screen.blit(background, (0, 0))

    # Looping through all the Events
    for event in pygame.event.get():

        # Check to Quit
        if event.type == pygame.QUIT:
            running = False

        # Check to detect a Keystroke
        if event.type == pygame.KEYDOWN:

            # Check to detect Left or Right key
            if event.key == pygame.K_LEFT:
                playerX_change = -3
            if event.key == pygame.K_RIGHT:
                playerX_change = 3
            if event.key == pygame.K_SPACE:
                if bullet_state == "Ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)
                    # Bullet sound
                    bullet_sound = mixer.Sound("Sounds\laser.wav")
                    bullet_sound.play()

        # Check to detect release of Keystroke
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Changing the player Co-ordinates while pressing a key
    playerX += playerX_change

    # Condition to avoid the player moving outside the window
    if playerX < 0:
        playerX = 0
    elif playerX > (800 - 64):  # 64 is the pixel of the player
        playerX = (800 - 64)

    # Changing the enemy Co-ordinates when hitting the boundary
    enemyX += enemyX_change

    # Speed multiplier
    if score_value > 99:
        if (score_value / prev_score_value) >= 2:
            prev_score_value = score_value
            speed_multiplier += 0.5

    # Enemy movement
    for i in range(num_of_enemies):
        # Game over condition
        if enemyY[i] > 430:  # 430
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_x:
                    running = False
                elif event.key == pygame.K_r:
                    score_value = 0
                    prev_score_value = 0.1
                    speed_multiplier = 1
                    for j in range(num_of_enemies):
                        enemyX[j] = random.randint(0, 800 - 64)
                        enemyY[j] = random.randint(50, 150)

        # Enemy boundary condition
        if enemyX[i] < 0:
            enemyX_change[i] = 1 * speed_multiplier
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] > (800 - 64):  # 64 is the pixel of the player
            enemyX_change[i] = -1 * speed_multiplier
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "Ready"
            score_value += 10
            enemyX[i] = random.randint(0, 800 - 64)
            enemyY[i] = random.randint(50, 150)
            # Explosion sound
            explosion_sound = mixer.Sound("Sounds\explosion.wav")
            explosion_sound.play()

        # Calling the enemy function
        enemy(enemyX[i], enemyY[i], i)

        # Changing the enemy Co-ordinates when hitting the boundary
        enemyX[i] += enemyX_change[i]

    # Calling the player function
    player(playerX, playerY)

    # Bullet Movement
    if bulletY <= -32:
        bulletY = 480
        bullet_state = "Ready"
    if bullet_state == "Fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Calling the score function
    show_score(textX, textY)

    # Updating the display
    pygame.display.update()
