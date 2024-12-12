import pygame
import math

# Initialize the pygame library
pygame.init()

# List to store all the painting actions (color, position, and shape)
painting = []

# Timer to control the frame rate
timer = pygame.time.Clock()
fps = 60  # Frames per second

# Default settings for color and shape
activeColor = (0, 0, 0)  # Black color
activeShape = 0  # Default shape is rectangle

# Screen dimensions
w = 800
h = 600

# Create a screen object with the given width and height
screen = pygame.display.set_mode([w, h])


# Function to draw the toolbar with color and shape options
def drawDisplay():
    # Draw the background of the toolbar (gray color)
    pygame.draw.rect(screen, 'gray', [0, 0, w, 100])
    # Draw the line separating the toolbar from the drawing area
    pygame.draw.line(screen, 'black', [0, 100], [w, 100])

    # Color buttons (rectangles)
    rect = [pygame.draw.rect(screen, 'black', [10, 10, 80, 80]), 0]
    pygame.draw.rect(screen, 'white', [20, 20, 60, 60])  # White rectangle

    # Circle button (black square with white circle)
    circ = [pygame.draw.rect(screen, 'black', [100, 10, 80, 80]), 1]
    pygame.draw.circle(screen, 'white', [140, 50], 30)  # Circle inside the rectangle

    # Right triangle button (black square with white triangle)
    right_triangle = [pygame.draw.rect(screen, 'black', [200, 10, 80, 80]), 2]
    pygame.draw.polygon(screen, 'white', [(w - 580, 70), (w - 580, 30), (w - 540, 30)])

    # Equilateral triangle button (black square with white triangle)
    equilateral_triangle = [pygame.draw.rect(screen, 'black', [290, 10, 80, 80]), 3]
    pygame.draw.polygon(screen, 'white', [[329, 20], [360, 70], [300, 70]])

    # Rhombus button (black square with white rhombus)
    rhombus = [pygame.draw.rect(screen, 'black', [380, 10, 80, 80]), 4]
    pygame.draw.polygon(screen, 'white', [(390, 50), (420, 70), (450, 50), (420, 30)])

    # Color selection buttons (colored squares)
    blue = [pygame.draw.rect(screen, (0, 0, 255), [w - 35, 10, 25, 25]), (0, 0, 255)]
    red = [pygame.draw.rect(screen, (255, 0, 0), [w - 35, 35, 25, 25]), (255, 0, 0)]
    green = [pygame.draw.rect(screen, (0, 255, 0), [w - 60, 10, 25, 25]), (0, 255, 0)]
    yellow = [pygame.draw.rect(screen, (255, 255, 0), [w - 60, 35, 25, 25]), (255, 255, 0)]
    black = [pygame.draw.rect(screen, (0, 0, 0), [w - 85, 10, 25, 25]), (0, 0, 0)]
    purple = [pygame.draw.rect(screen, (255, 0, 255), [w - 85, 35, 25, 25]), (255, 0, 255)]
    eraser = [pygame.draw.rect(screen, (255, 255, 255), [w - 150, 20, 25, 25]), (255, 255, 255)]  # Eraser (white)

    # Return color and shape buttons for collision detection later
    return [blue, red, green, yellow, black, purple, eraser], [rect, circ, right_triangle, equilateral_triangle, rhombus]


# Function to draw the paintings (shapes drawn by the user)
def drawPaint(paints):
    for paint in paints:
        if paint[2] == 1:
            # Draw a circle with the specified color and position
            pygame.draw.circle(screen, paint[0], paint[1], 15)
        elif paint[2] == 0:
            # Draw a rectangle with the specified color and position
            pygame.draw.rect(screen, paint[0], [paint[1][0] - 15, paint[1][1] - 15, 30, 30])
        elif paint[2] == 2:
            # Draw a right triangle
            pygame.draw.polygon(screen, paint[0], [(paint[1][0], paint[1][1]), (paint[1][0] - 30, paint[1][1] + 30), (paint[1][0], paint[1][1] + 30)])
        elif paint[2] == 3:
            # Draw an equilateral triangle
            side_length = 30
            height = (math.sqrt(3) / 2) * side_length
            pygame.draw.polygon(screen, paint[0], [(paint[1][0], paint[1][1]), (paint[1][0] + side_length / 2, paint[1][1] + height), (paint[1][0] - side_length / 2, paint[1][1] + height)])
        elif paint[2] == 4:
            # Draw a rhombus
            pygame.draw.polygon(screen, paint[0], [(paint[1][0], paint[1][1]), (paint[1][0] + 30, paint[1][1] + 15), (paint[1][0], paint[1][1] + 30), (paint[1][0] - 30, paint[1][1] + 15)])


# Function to handle drawing based on the selected shape
def draw():
    global activeColor, activeShape, mouse
    if mouse[1] > 100:  # Only allow drawing below the toolbar
        if activeShape == 0:
            # Draw a rectangle
            pygame.draw.rect(screen, activeColor, [mouse[0] - 15, mouse[1] - 15, 30, 30])
        elif activeShape == 1:
            # Draw a circle
            pygame.draw.circle(screen, activeColor, mouse, 15)
        elif activeShape == 2:
            # Draw a right triangle
            pygame.draw.polygon(screen, activeColor, [(mouse[0], mouse[1]), (mouse[0] - 30, mouse[1] + 30), (mouse[0], mouse[1] + 30)])
        elif activeShape == 3:
            # Draw an equilateral triangle
            side_length = 30
            height = (math.sqrt(3) / 2) * side_length
            pygame.draw.polygon(screen, activeColor, [(mouse[0], mouse[1]), (mouse[0] + side_length / 2, mouse[1] + height), (mouse[0] - side_length / 2, mouse[1] + height)])
        elif activeShape == 4:
            # Draw a rhombus
            pygame.draw.polygon(screen, activeColor, [(mouse[0], mouse[1]), (mouse[0] + 30, mouse[1] + 15), (mouse[0], mouse[1] + 30), (mouse[0] - 30, mouse[1] + 15)])


# Main loop for running the program
run = True
while run:
    timer.tick(fps)  # Control the frame rate
    screen.fill('white')  # Fill the screen with a white background
    colors, shape = drawDisplay()  # Draw the toolbar and get the buttons

    mouse = pygame.mouse.get_pos()  # Get the current position of the mouse
    draw()  # Draw the selected shape at the mouse position

    # Check if the left mouse button is clicked
    click = pygame.mouse.get_pressed()[0]
    if click and mouse[1] > 100:  # Only allow painting below the toolbar
        # Append the color, position, and shape to the painting list
        painting.append((activeColor, mouse, activeShape))
    
    # Draw all the previously drawn paintings
    drawPaint(painting)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False  # Exit the program if the window is closed

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Clear the screen when the spacebar is pressed
                painting = []

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if any of the color buttons was clicked
            for i in colors:
                if i[0].collidepoint(event.pos):  # If mouse click is inside the button
                    activeColor = i[1]  # Set the active color

            # Check if any of the shape buttons was clicked
            for i in shape:
                if i[0].collidepoint(event.pos):  # If mouse click is inside the button
                    activeShape = i[1]  # Set the active shape

    pygame.display.flip()  # Update the screen with the latest changes
