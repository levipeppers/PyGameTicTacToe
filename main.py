import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
LINE_COLOR = (255, 255, 255)
LINE_WIDTH = 10

# Constants for X and O
X_COLOR = (255, 0, 0)
O_COLOR = (0, 0, 255)
CELL_SIZE = WIDTH // 3

# Grid state
grid = [[None, None, None], [None, None, None], [None, None, None]]

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic Tac Toe")

def draw_grid():
    # Draw vertical lines
    pygame.draw.line(screen, LINE_COLOR, (WIDTH // 3, 0), (WIDTH // 3, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * WIDTH // 3, 0), (2 * WIDTH // 3, HEIGHT), LINE_WIDTH)
    # Draw horizontal lines
    pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT // 3), (WIDTH, HEIGHT // 3), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * HEIGHT // 3), (WIDTH, 2 * HEIGHT // 3), LINE_WIDTH)

def draw_xo():
    for row in range(3):
        for col in range(3):
            if grid[row][col] == 'X':
                draw_x(row, col)
            elif grid[row][col] == 'O':
                draw_o(row, col)

def draw_x(row, col):
    start_pos = (col * CELL_SIZE + 20, row * CELL_SIZE + 20)
    end_pos = ((col + 1) * CELL_SIZE - 20, (row + 1) * CELL_SIZE - 20)
    pygame.draw.line(screen, X_COLOR, start_pos, end_pos, LINE_WIDTH)
    start_pos = (col * CELL_SIZE + 20, (row + 1) * CELL_SIZE - 20)
    end_pos = ((col + 1) * CELL_SIZE - 20, row * CELL_SIZE + 20)
    pygame.draw.line(screen, X_COLOR, start_pos, end_pos, LINE_WIDTH)

def draw_o(row, col):
    center = (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2)
    pygame.draw.circle(screen, O_COLOR, center, CELL_SIZE // 2 - 20, LINE_WIDTH)

def handle_click(pos):
    row = pos[1] // CELL_SIZE
    col = pos[0] // CELL_SIZE
    if grid[row][col] is None:
        grid[row][col] = 'X'
    elif grid[row][col] == 'X':
        grid[row][col] = 'O'
    else:
        grid[row][col] = None

def main():
    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_click(event.pos)

        # Fill the screen with black
        screen.fill((0, 0, 0))

        # Draw the grid
        draw_grid()
        draw_xo()

        # Update the display
        pygame.display.flip()

if __name__ == "__main__":
    main()
