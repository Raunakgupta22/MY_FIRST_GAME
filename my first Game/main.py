import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 700, 650     
WHITE = (40, 135, 218  )
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
FPS = 30

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Define Bird class
class Bird:
    def __init__(self):
        self.x = 50                  # Initial X position of the bird
        self.y = HEIGHT // 2         # Initial Y position of the bird
        self.velocity = 0            # Initial velocity of the bird
        self.gravity = 1             # Gravity effect (adjusted for faster falling)
        self.lift = -10              # Lift when bird flaps its wings
        self.image = pygame.image.load("bird.png")  # Load bird image

    def flap(self):
        # When the bird flaps, it goes up by reducing velocity
        self.velocity += self.lift

    def update(self):
        # Update bird's position by adding velocity
        self.velocity += self.gravity
        self.velocity *= 0.9        # Add damping factor for smoother movement
        self.y += self.velocity

    def draw(self):
        # Draw the bird on the screen
        screen.blit(self.image, (self.x, self.y))

# Define Pipe class
class Pipe:
    def __init__(self):
        self.gap = 200               # Gap between upper and lower pipes
        self.width = 50              # Width of the pipes
        self.x = WIDTH                # Initial X position of the pipes
        self.speed = 5               # Speed at which pipes move horizontally
        self.top_height = random.randint(50, HEIGHT - self.gap - 50)  # Random height for upper pipe
        self.bottom_height = HEIGHT - self.gap - self.top_height     # Calculate height for lower pipe
        self.passed = False          # Attribute to track if the bird passed through the pipe

    def update(self):
        # Update pipes' position by moving them to the left
        self.x -= self.speed

    def draw(self):
        # Draw upper pipe
        pygame.draw.rect(screen, GREEN, (self.x, 0, self.width, self.top_height))
        # Draw lower pipe
        pygame.draw.rect(screen, GREEN, (self.x, self.top_height + self.gap, self.width, self.bottom_height))

# Define Button class
class Button:
    def __init__(self, x, y, width, height, color, text, text_color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.text_color = text_color
        self.action = action

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)
        font = pygame.font.SysFont(None, 36)
        text = font.render(self.text, True, self.text_color)
        text_rect = text.get_rect(center=self.rect.center)
        screen.blit(text, text_rect)

# Initialize game objects
bird = Bird()               # Create bird object
pipes = []                  # List to store pipes
score = 0                   # Player score
game_started = False        # Flag to indicate if the game has started

# Create start button
start_button = Button(WIDTH // 2 - 75, HEIGHT // 2, 150, 50, GREEN, "Start", BLACK)

# Create quit button
quit_button = Button(WIDTH // 2 - 75, HEIGHT // 2 + 100, 150, 50, RED, "Quit", BLACK)

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_started:
            if start_button.rect.collidepoint(event.pos):
                game_started = True
            elif quit_button.rect.collidepoint(event.pos):
                running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_started:
                bird.flap()

    # Update game objects if game has started
    if game_started:
        bird.update()
        # Other game updates...

    # Create new pipes
    if game_started and (len(pipes) == 0 or pipes[-1].x < WIDTH - 200):
        pipes.append(Pipe())

    # Update and draw pipes
    for pipe in pipes:
        pipe.update()
        pipe.draw()

        # Check collision with bird
        if game_started and bird.x + 30 > pipe.x and bird.x < pipe.x + pipe.width:
            if bird.y < pipe.top_height or bird.y + 30 > pipe.top_height + pipe.gap:
                running = False

        # Increment score when bird passes through the pipe
        if game_started and pipe.x + pipe.width < bird.x and not pipe.passed:
            pipe.passed = True
            score += 1

    # Draw bird
    bird.draw()

    # Draw buttons only if game hasn't started
    if not game_started:
        start_button.draw()
        quit_button.draw()

    # Draw score
    if game_started:
        font = pygame.font.SysFont(None, 36)
        text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(text, (10, 10))
    
    pygame.display.flip()   # Update the display
    screen.fill(WHITE)      # Fill the screen with white
    clock.tick(FPS)         # Control the frame rate

# Quit Pygame
pygame.quit()
sys.exit()
