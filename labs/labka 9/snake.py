import pygame
import random

# Initialize Pygame
pygame.init()

# Define screen dimensions and grid size
WIDTH, HEIGHT = 600, 400
GRIDSIZE = 20  # Size of each grid square in pixels
GRIDWIDTH, GRIDHEIGHT = WIDTH // GRIDSIZE, HEIGHT // GRIDSIZE  # Number of grid cells in both directions

# Define colors (RGB format)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Define direction vectors for the snake (UP, DOWN, LEFT, RIGHT)
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Function to render text on the screen
def drawtext(surface, text, size, x, y):
    font = pygame.font.SysFont('Arial', size)  # Create a font object
    textsurface = font.render(text, True, WHITE)  # Render the text (white color)
    textrect = textsurface.get_rect()  # Get the rectangle for the text
    textrect.center = (x, y)  # Position the text at the specified coordinates
    surface.blit(textsurface, textrect)  # Draw the text on the surface

# Function to draw the apple (food) on the screen
def drawapple(surface, apple):
    pygame.draw.rect(surface, apple[1], (apple[0][0]*GRIDSIZE, apple[0][1]*GRIDSIZE, GRIDSIZE, GRIDSIZE))  # Draw the apple as a rectangle

# Function to draw the snake on the screen
def drawsnake(surface, snake):
    for seg in snake:  # Loop through each segment of the snake
        pygame.draw.rect(surface, WHITE, (seg[0]*GRIDSIZE, seg[1]*GRIDSIZE, GRIDSIZE, GRIDSIZE))  # Draw each segment as a white square

def main():
    # Set up the screen and window caption
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Snake')

    # Initial snake position (center of the grid) and direction
    snake = [(GRIDWIDTH // 2, GRIDHEIGHT // 2)]  
    snake_direction = RIGHT  # Start moving to the right
    apple = ((random.randint(0, GRIDWIDTH-1), random.randint(0, GRIDHEIGHT-1)), RED)  # Random initial apple position and color
    running = True  # Game is running
    sum_food = 0  # Counter for the number of apples eaten
    level = 1  # Initial game level
    delay = 110  # Delay between frames, controls the game speed
    food_collec = 0  # Total score, based on the type of food eaten
    food_timer = 3000  # Time limit for food appearance (in milliseconds)
    food_timer_start = pygame.time.get_ticks()  # Get the current time in milliseconds to track food expiration

    while running:
        for event in pygame.event.get():  # Event handling loop
            if event.type == pygame.QUIT:  # If the player closes the window
                running = False
            elif event.type == pygame.KEYDOWN:  # If a key is pressed
                # Change snake direction based on key input, ensuring the snake cannot reverse
                if event.key == pygame.K_UP and snake_direction != DOWN:
                    snake_direction = UP
                elif event.key == pygame.K_DOWN and snake_direction != UP:
                    snake_direction = DOWN
                elif event.key == pygame.K_LEFT and snake_direction != RIGHT:
                    snake_direction = LEFT
                elif event.key == pygame.K_RIGHT and snake_direction != LEFT:
                    snake_direction = RIGHT

        # Calculate the new head position based on the current direction
        newhead = (snake[0][0] + snake_direction[0], snake[0][1] + snake_direction[1])
        snake.insert(0, newhead)  # Add the new head at the front of the snake

        # Check if the snake runs into the walls of the screen (game over)
        if not (0 <= newhead[0] < GRIDWIDTH) or not (0 <= newhead[1] < GRIDHEIGHT):
            running = False

        # Check if the snake runs into itself (game over)
        if len(snake) != len(set(snake)):  # If there are duplicate segments, the snake has collided with itself
            running = False

        # Check if the snake eats an apple
        if newhead == apple[0]:
            if apple[1] == RED:  # Red apples are worth 1 point
                score = 1
            elif apple[1] == GREEN:  # Green apples are worth 2 points
                score = 2
            elif apple[1] == BLUE:  # Blue apples are worth 3 points
                score = 3

            # Generate a new apple at a random position with a random color
            apple = ((random.randint(0, GRIDWIDTH-1), random.randint(0, GRIDHEIGHT-1)), random.choice([RED, GREEN, BLUE]))
            sum_food += 1  # Increment the food counter
            food_collec += score  # Add the score to the total
            food_timer_start = pygame.time.get_ticks()  # Reset the food timer
        else:
            snake.pop()  # Remove the last segment of the snake (it didn't eat food)

        # Fill the screen with black color and draw all game elements
        screen.fill(BLACK)
        drawsnake(screen, snake)  # Draw the snake
        drawapple(screen, apple)  # Draw the apple
        drawtext(screen, f"Your level: {level}", 20, WIDTH - 60, 30)  # Display the level
        drawtext(screen, f"Foods collected: {food_collec}", 20, WIDTH - 80, 60)  # Display the total score
        pygame.display.flip()  # Update the display

        # If the player has eaten 3 pieces of food, increase the level
        if sum_food == 3:
            sum_food = 0
            level += 1  # Increase the level
            delay = max(delay - 10, 50)  # Decrease the delay (increase speed), but not below 50ms

        # If the food timer exceeds the threshold, generate a new apple
        if pygame.time.get_ticks() - food_timer_start >= food_timer:
            apple = ((random.randint(0, GRIDWIDTH-1), random.randint(0, GRIDHEIGHT-1)), random.choice([RED, GREEN, BLUE]))
            food_timer_start = pygame.time.get_ticks()  # Reset the food timer

        pygame.time.delay(delay)  # Delay to control game speed

    # Game over screen
    screen.fill(BLACK)
    drawtext(screen, "Game Over", 50, WIDTH//2, HEIGHT//2)  # Display "Game Over" message
    pygame.display.flip()  # Update the display
    pygame.time.delay(2000)  # Wait for 2 seconds before quitting

    pygame.quit()  # Quit Pygame

# Run the main game loop
main()
