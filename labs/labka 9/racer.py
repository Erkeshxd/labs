import pygame, sys
from pygame.locals import *
import random, time

# Initialize pygame
pygame.init()

# Set FPS and the clock to control the frame rate
FPS = 60
FramePerSec = pygame.time.Clock()

# Define some colors for the game (RGB format)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set the screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5  # Starting speed of the falling objects
SCORE = 0  # Initial score
coin2 = 0  # Counter for collecting coins

# Define fonts for rendering text
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)

# Text to display when the game is over
game_over = font.render("Game Over", True, BLACK)

# Load the background image
background = pygame.image.load(r"C:\Users\Пользователь\Desktop\clock\labka 9\road.jpg")

# Set up the display surface (the game window)
DISPLAYSURF = pygame.display.set_mode((400, 600))
DISPLAYSURF.fill(WHITE)  # Fill the screen with white initially
pygame.display.set_caption("Game")  # Set the window title

# Define the Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load the enemy image (red car)
        self.image = pygame.image.load(r"C:\Users\Пользователь\Desktop\clock\labka 9\redcar.jpg")
        self.rect = self.image.get_rect()  # Get the rectangle around the image for positioning
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)  # Randomize the enemy's initial position

    def move(self):
        global SCORE
        # Move the enemy down by the speed value
        self.rect.move_ip(0, SPEED)
        if self.rect.top > 600:  # If the enemy has passed the bottom of the screen
            SCORE += 1  # Increase the score
            self.rect.top = 0  # Reset the position to the top
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)  # New random position

# Define the Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load the player image (blue car)
        self.image = pygame.image.load(r"C:\Users\Пользователь\Desktop\clock\labka 9\bluecar.jpg")
        self.rect = self.image.get_rect()  # Get the rectangle around the image for positioning
        self.rect.center = (160, 520)  # Initial position of the player car

    def move(self):
        pressed_keys = pygame.key.get_pressed()  # Get the current state of all keys
        if self.rect.left > 0:  # Check if the player is not at the left edge
            if pressed_keys[K_LEFT]:  # If the left arrow key is pressed
                self.rect.move_ip(-5, 0)  # Move left
        if self.rect.right < SCREEN_WIDTH:  # Check if the player is not at the right edge
            if pressed_keys[K_RIGHT]:  # If the right arrow key is pressed
                self.rect.move_ip(5, 0)  # Move right

# Define the Coin class
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load the coin image
        self.image = pygame.image.load(r"C:\Users\Пользователь\Desktop\clock\labka 9\coin.jpg")
        self.rect = self.image.get_rect()  # Get the rectangle around the image for positioning
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)  # Random initial position at the top

    def reset(self):
        # Reset the coin's position to the top of the screen
        self.rect.top = 0
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        # Move the coin down by the speed value
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:  # If the coin has passed the bottom of the screen
            self.reset()  # Reset its position

# Define the BigCoin class (special large coin)
class BigCoin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Load the big coin image
        self.image = pygame.image.load(r"C:\Users\Пользователь\Desktop\clock\labka 9\coin.jpg")
        self.rect = self.image.get_rect()  # Get the rectangle around the image for positioning

    def move(self):
        # Move the big coin down by the speed value
        self.rect.move_ip(0, SPEED)

# Create instances of the player, enemy, coin, and big coin
P1 = Player()
E1 = Enemy()
C1 = Coin()
B1 = BigCoin()

# Create sprite groups for enemies, coins, and big coins
enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coins.add(C1)

big_coins = pygame.sprite.Group()
big_coins.add(B1)

# Create a group to hold all sprites (for easy updating and drawing)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1, C1, B1, E1)

# Set a timer event to gradually increase the speed
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:  # Increase speed every 1000 milliseconds (1 second)
            SPEED += 0.5
        if event.type == QUIT:  # Handle quitting the game
            pygame.quit()
            sys.exit()

    # Draw the background image
    DISPLAYSURF.blit(background, (0, 0))

    # Render the score and coin counter text
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))

    # Render the coin counter text
    counter = font_small.render(str(coin2), True, BLACK)
    DISPLAYSURF.blit(counter, (380, 10))

    # Check for collisions with coins (and update coin counter)
    collided_coins = pygame.sprite.spritecollide(P1, coins, True)
    for coin in collided_coins:
        coin2 += 1  # Increase coin counter
        new_coin = Coin()  # Create a new coin
        coins.add(new_coin)  # Add it to the coin group
        all_sprites.add(new_coin)  # Add it to all sprites group
        new_coin.rect.top = 0  # Reset the coin's position
        new_coin.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)  # Random position
        if coin2 % 10 == 0:  # Every 10 coins, increase the speed and spawn a big coin
            SPEED += 1
            new_coin = BigCoin()  # Create a new big coin
            big_coins.add(new_coin)  # Add it to the big coins group
            all_sprites.add(new_coin)  # Add it to all sprites group
            new_coin.rect.top = 0  # Reset its position
            new_coin.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)  # Random position

    # Check for collisions with big coins (and increase coin counter by 5)
    big_coins_collided = pygame.sprite.spritecollide(P1, big_coins, True)
    for big_coin in big_coins_collided:
        coin2 += 5  # Increase coin counter by 5
        big_coin.kill()  # Remove the big coin from the game

    # Move all sprites (player, enemies, coins, etc.)
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)  # Draw the sprite's image
        entity.move()  # Update the sprite's position

    # Check for collisions between the player and enemies
    if pygame.sprite.spritecollideany(P1, enemies):
        # Play crash sound and display game over
        pygame.mixer.Sound("c:\\Users\\Admin\\OneDrive\\Рабочий стол\\Lab 9\\racer\\crash.wav").play()
        time.sleep(0.5)

        # Display "Game Over" text and fill screen with red
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()

        # Remove all sprites from the game (end the game)
        for entity in all_sprites:
            entity.kill()

        # Wait for a bit before quitting
        time.sleep(2)
        pygame.quit()
        sys.exit()

    pygame.display.update()  # Update the display
    FramePerSec.tick(FPS)  # Control the frame rate
