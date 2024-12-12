import psycopg2
from config import config  # Importing the database configuration function
from os import scandir
import pygame
import random
import sys
import threading
import time
import os

# Constants for the game's configuration
BLACK = (0, 0, 0)  # Color of the game screen background (Black)
LINE_COLOR = (50, 50, 50)  # Grid line color
HEIGHT = 400  # Game window height in pixels
WIDTH = 400  # Game window width in pixels
SPEED = 5  # Initial speed of the snake
BLOCK_SIZE = 20  # Size of the grid blocks (each cell is 20x20 pixels)
MAX_LEVEL = 2  # Maximum number of levels in the game
SCORE = 0  # Initial score of the player
LEVEL = 1  # Initial level

# Print the current working directory to the console
print("Текущая рабочая директория:", os.getcwd())

# Database interaction functions

def get_player(nickname):
    """
    Fetch the player data (level and score) from the database based on their nickname.
    """
    sql = "SELECT * FROM Snake WHERE NickName = %s"  # SQL query to select player by nickname
    conn = None
    try:
        params = config()  # Fetch the database connection parameters
        conn = psycopg2.connect(**params)  # Establish a connection to the database
        cur = conn.cursor()  # Create a cursor to execute SQL queries
        cur.execute(sql, (nickname,))  # Execute the query with the given nickname
        row = cur.fetchone()  # Fetch the first matching row

        if row:  # If the player exists
            return row[1], row[2]  # Return the player's level and score
        else:
            return None, None  # Return None if the player does not exist

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)  # Print any errors that occur
    finally:
        if conn is not None:
            conn.close()  # Ensure the database connection is closed

def insert_player(players):
    """
    Insert or update player data (nickname, level, score) in the database.
    """
    conn = None
    try:
        params = config()  # Fetch the database connection parameters
        conn = psycopg2.connect(**params)  # Establish a connection to the database
        cur = conn.cursor()  # Create a cursor to execute SQL queries

        for player in players:  # Loop through each player in the list
            nickname, level, score = player
            # Check if the player already exists in the database
            cur.execute("SELECT * FROM Snake WHERE NickName = %s", (nickname,))
            row = cur.fetchone()

            if row:  # If the player exists, update their level and score
                cur.execute("UPDATE Snake SET Level = %s, Score = %s WHERE NickName = %s", 
                            (level, score, nickname))
            else:  # If the player does not exist, insert a new player into the database
                cur.execute("INSERT INTO Snake(NickName, Level, Score) VALUES(%s, %s, %s)", 
                            (nickname, level, score))
        conn.commit()  # Commit changes to the database

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)  # Print any errors that occur
    finally:
        if conn is not None:
            conn.close()  # Ensure the database connection is closed

# Player input logic
if __name__ == '__main__':
    print("1) New Player 2) I have an account: ")
    option = int(input())  # Prompt the user to select an option (New Player or Existing Account)
    
    if option == 1:
        # If the user is a new player
        Nickname = str(input("Enter a nickname: "))  # Prompt for a nickname
        print("Completed!")
        
    elif option == 2:
        while True:
            # If the user already has an account, ask for their nickname
            Nickname = str(input("Enter your nickname: "))
            LEVEL, SCORE = get_player(Nickname)  # Get the player's level and score from the database
            
            if LEVEL is None:
                print("User doesn't exist")  # If the player doesn't exist, notify them
            else:
                break  # If the player exists, break out of the loop
    else:
        print("Invalid option is selected")  # If an invalid option is selected
        sys.exit()  # Exit the program

# Helper classes for the game mechanics

class Point:
    """
    A class to represent a point (x, y) in the game grid.
    """
    def __init__(self, _x, _y):
        self.x = _x  # X-coordinate
        self.y = _y  # Y-coordinate

class Wall:
    """
    A class to represent the walls of the game level.
    The walls are loaded from a level file.
    """
    def __init__(self, level):
        self.body = []  # List to store the wall points
        level = level % MAX_LEVEL  # Limit the levels to MAX_LEVEL
        try:
            with open(r"C:\Users\Пользователь\Desktop\clock\levels\level0.txt", "r") as f:
                # Open the file for the current level
                for y, line in enumerate(f):  # Loop through the file line by line
                    for x, char in enumerate(line.strip()):  # Loop through each character in the line
                        if char == '#':  # If the character is a wall ('#')
                            self.body.append(Point(x, y))  # Add the point to the wall list
        except FileNotFoundError:
            print(f"Error: Level file levels/level{level}.txt not found.")
            sys.exit()  # If the level file is not found, exit the game

# Food class for handling food objects that the snake eats
class Food:
    def __init__(self, wall):
        self.body = None  # The food's position
        self.wall = wall  # The walls of the current level
        self.lock = threading.Lock()  # A lock to handle thread safety when updating the food position
        self.update_locationfirst()  # Initialize the food location
        self.update_locationsecond()  # Set a second location update for randomness

    def update_locationfirst(self):
        self.lock.acquire()  # Acquire the lock to ensure thread safety
        while True:
            # Randomly generate a new food location
            self.body = Point(random.randint(0, WIDTH//BLOCK_SIZE-1), random.randint(0, HEIGHT//BLOCK_SIZE-1))
            # Ensure the food doesn't overlap with any walls
            if not any(point.x == self.body.x and point.y == self.body.y for point in self.wall.body):
                break
        self.lock.release()  # Release the lock after updating the location
        # Periodically update the food location every 5-10 seconds
        self.timer = threading.Timer(random.randrange(5, 10), self.update_locationfirst)
        self.timer.start()

    def update_locationsecond(self):
        while True:
            # Randomly generate a new food location (second version for the second timer)
            self.body = Point(random.randint(0, WIDTH//BLOCK_SIZE-1), random.randint(0, HEIGHT//BLOCK_SIZE-1))
            # Ensure the food doesn't overlap with any walls
            if not any(point.x == self.body.x and point.y == self.body.y for point in self.wall.body):
                break

    def draw(self):
        """
        Draw the food on the screen as a rectangle.
        """
        rect = pygame.Rect(BLOCK_SIZE * self.body.x, BLOCK_SIZE * self.body.y, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(SCREEN, (0, 255, 0), rect)  # Draw food as green rectangle

    def move(self):
        """
        Move the food to a new random location.
        """
        self.update_locationsecond()

# Snake class for handling the snake's movement and growth
class Snake:
    def __init__(self):
        self.body = [Point(10, 11)]  # Initial position of the snake (head at (10, 11))
        self.dx = 0  # Initial movement in the x-direction (no movement)
        self.dy = 0  # Initial movement in the y-direction (no movement)
        self.level = 0  # Initial level

    def game_over(self):
        """
        Handle game over scenario by saving player data and displaying a game over message.
        """
        global LEVEL
        insert_player([(Nickname, LEVEL, SCORE)])  # Save player score and level to database
        font = pygame.font.SysFont("Verdana", 30)
        text = font.render("GAME OVER", True, (255, 255, 255))  # Render game over text
        text_rect = text.get_rect(center=(WIDTH/2, HEIGHT/2))  # Center the text on the screen
        SCREEN.blit(text, text_rect)  # Draw the text on the screen
        pygame.display.flip()
        time.sleep(2)  # Wait for 2 seconds to show the game over message
        pygame.quit()  # Close pygame window
        sys.exit()  # Exit the program

    def move(self, wall):
        """
        Move the snake in the current direction and check for collisions with walls or self.
        """
        # Move each part of the snake (except for the head)
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i-1].x
            self.body[i].y = self.body[i-1].y

        # Move the head in the specified direction
        self.body[0].x += self.dx 
        self.body[0].y += self.dy 

        # Handle snake wrapping around the screen
        if self.body[0].x * BLOCK_SIZE > WIDTH:
            self.body[0].x = 0
    
        if self.body[0].y * BLOCK_SIZE > HEIGHT:
            self.body[0].y = 0

        if self.body[0].x < 0:
            self.body[0].x = WIDTH / BLOCK_SIZE
    
        if self.body[0].y < 0:
            self.body[0].y = HEIGHT / BLOCK_SIZE

        # Check for collision with walls
        for point in wall.body:
            if self.body[0].x == point.x and self.body[0].y == point.y and not (self.body[0].x == 0 or self.body[0].y == 0 or self.body[0].x == WIDTH//BLOCK_SIZE or self.body[0].y == HEIGHT//BLOCK_SIZE):
                self.game_over()  # End game if snake collides with the wall

    def draw(self):
        """
        Draw the snake on the screen.
        """
        # Draw the snake's head
        point = self.body[0]
        rect = pygame.Rect(BLOCK_SIZE * point.x, BLOCK_SIZE * point.y, BLOCK_SIZE, BLOCK_SIZE)
        pygame.draw.rect(SCREEN, (255, 0, 0), rect)  # Head is red

        # Draw the snake's body
        for point in self.body[1:]:
            rect = pygame.Rect(BLOCK_SIZE * point.x, BLOCK_SIZE * point.y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(SCREEN, (0, 255, 0), rect)  # Body is green

    def check_collision(self, food):
        """
        Check if the snake eats the food.
        """
        if self.body[0].x == food.body.x and self.body[0].y == food.body.y:
            food_score = random.randrange(1, 4)  # Random score for the food
            global SCORE
            SCORE += food_score  # Add the score
            food.move()  # Move the food to a new location
            # Grow the snake by adding a new point to the head
            self.body.insert(0, Point(self.body[0].x + self.dx, self.body[0].y + self.dy))

    def shorten(self):
        """
        Shorten the snake by removing the last segment.
        """
        self.body.pop()  # Remove the last segment of the snake's body

# Main function to run the game
def main():
    global SCREEN, CLOCK, SPEED, LEVEL
    
    pygame.init()  # Initialize pygame

    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))  # Create the game window
    CLOCK = pygame.time.Clock()  # Create the clock to control the game's frame rate
    SCREEN.fill(BLACK)  # Fill the screen with black background
    font_small = pygame.font.SysFont("Verdana", 15)  # Font for displaying score and level

    # Initialize the game components (snake, walls, food)
    snake = Snake()
    wall = Wall(snake.level)
    food = Food(wall) 

    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                insert_player([(Nickname, LEVEL, SCORE)])  # Save player data before quitting
                pygame.quit()  # Quit pygame
                sys.exit()  # Exit the program
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    snake.dx = 1  # Move snake to the right
                    snake.dy = 0
                if event.key == pygame.K_LEFT:
                    snake.dx = -1  # Move snake to the left
                    snake.dy = 0
                if event.key == pygame.K_UP:
                    snake.dx = 0  # Move snake up
                    snake.dy = -1
                if event.key == pygame.K_DOWN:
                    snake.dx = 0  # Move snake down
                    snake.dy = 1

        # Level progression logic (after snake reaches a certain size)
        if len(snake.body) > 4 and len(snake.body) % 2 == 1:
            newLevel = snake.level + 1
            LEVEL += 1
            SPEED += 1  # Increase speed as the level increases
            snake = Snake()  # Reset snake
            snake.level = newLevel  # Set new level for the snake
            wall = Wall(snake.level)  # Load new walls for the new level
            food = Food(wall)  # Load new food for the new level

        # Update the game state
        snake.move(wall)
        food.lock.acquire()  # Acquire lock to safely update food position
        snake.check_collision(food)  # Check if snake eats the food
        food.lock.release()  # Release lock after updating food position

        # Redraw the game screen
        SCREEN.fill(BLACK)  # Clear the screen
        wall.draw()  # Draw walls
        food.draw()  # Draw food
        snake.draw()  # Draw snake
        drawGrid()  # Draw the game grid

        # Display score and level
        score_surface = font_small.render("SCORE: " + str(SCORE), True, (255, 255, 255)) 
        SCREEN.blit(score_surface, (305, 5))

        level_surface = font_small.render("Level: " + str(LEVEL), True, (255, 255, 255)) 
        SCREEN.blit(level_surface, (10, 5))
        
        pygame.display.update()  # Update the display
        CLOCK.tick(SPEED + LEVEL - 1)  # Control game speed

# Function to draw the grid on the screen
def drawGrid():
    for x in range(0, WIDTH, BLOCK_SIZE):
        for y in range(0, HEIGHT, BLOCK_SIZE):
            rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
            pygame.draw.rect(SCREEN, LINE_COLOR, rect, 1)  # Draw grid lines

# Start the game
main()

