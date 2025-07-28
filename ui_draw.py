import pygame
import sys

# Init pygame
pygame.init()

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 1280, 720
CELL_SIZE = 10
ROWS = WINDOW_HEIGHT // CELL_SIZE
COLS = WINDOW_WIDTH // CELL_SIZE
BG_COLOR = (91, 112, 0)  # #5B7000
BLACK = (0, 0, 0)

# Setup
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("UI DRAW")

# Track clicked cells (True = black, False = bg)
grid = [[False for i in range(COLS)] for i in range(ROWS)]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            col = x // CELL_SIZE
            row = y // CELL_SIZE
            if 0 <= col < COLS and 0 <= row < ROWS:
                grid[row][col] = not grid[row][col]  # toggle

    # Draw background
    screen.fill(BG_COLOR)

    # Draw cells
    for row in range(ROWS):
        for col in range(COLS):
            if grid[row][col]:
                pygame.draw.rect(
                    screen,
                    BLACK,
                    (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                )

    # Draw grid lines (optional)
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, (40, 40, 40), (0, y), (WINDOW_WIDTH, y))

    pygame.display.flip()

pygame.quit()
sys.exit()
