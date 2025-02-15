import pygame
import random
import math

# Initialize pygame
pygame.init()

# Constants for the game
SIZE = 4  # Size of the grid
TILE_SIZE = 150 # Size of each tile
TILE_MARGIN = 7  # Margin between tiles
GRID_SIZE = SIZE * (TILE_SIZE + TILE_MARGIN) + TILE_MARGIN  # Total size of the grid
FONT_SIZE = 50  # Font size for tile numbers
SCORE_FONT_SIZE = 30  # Font size for the score display
BACKGROUND_COLOR = (187, 173, 160)  # Background color of the game
TILE_COLORS = {  # Colors for different tile values
    0: (204, 192, 179),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}
FONT_COLOR = (119, 110, 101)  # Color of the font for tile numbers

# Set up the display
screen = pygame.display.set_mode((GRID_SIZE, GRID_SIZE + 50))
pygame.display.set_caption('2048')

# Load fonts for numbers and score
font = pygame.font.Font(None, FONT_SIZE)
score_font = pygame.font.Font(None, SCORE_FONT_SIZE)

class Game2048:
    def __init__(self):
        self.grid = [[0] * SIZE for _ in range(SIZE)]  # Initialize the grid with zeros
        self.score = 0  # Initialize the score
        self.over = False  # Game over flag
        self.won = False  # Game won flag
        self.init_game()  # Start the game

    def init_game(self):
        self.add_new_tile()  # Add the first tile
        self.add_new_tile()  # Add the second tile
        self.draw_grid()  # Draw the initial grid

    def add_new_tile(self):
        # Find all empty cells
        empty_cells = [(i, j) for i in range(SIZE) for j in range(SIZE) if self.grid[i][j] == 0]
        if empty_cells:
            # Choose a random empty cell and set it to 2 or 4
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 4 if random.random() >= 0.9 else 2

    def draw_grid(self):
        screen.fill(BACKGROUND_COLOR)  # Fill the background
        for i in range(SIZE):
            for j in range(SIZE):
                value = self.grid[i][j]
                color = TILE_COLORS.get(value, TILE_COLORS[2048])  # Get the color for the tile value
                rect = pygame.Rect(
                    TILE_MARGIN + j * (TILE_SIZE + TILE_MARGIN),
                    TILE_MARGIN + i * (TILE_SIZE + TILE_MARGIN) + 50,
                    TILE_SIZE,
                    TILE_SIZE
                )
                pygame.draw.rect(screen, color, rect)  # Draw the tile
                if value:
                    text = font.render(str(value), True, FONT_COLOR)  # Render the number
                    text_rect = text.get_rect(center=rect.center)  # Center the number in the tile
                    screen.blit(text, text_rect)  # Draw the number on the tile
        
        # Draw score
        score_text = score_font.render(f'Score: {self.score}', True, FONT_COLOR)
        screen.blit(score_text, (10, 10))
        
        pygame.display.update()  # Update the display

    def compress(self, row):
        # Compress the row by moving all non-zero elements to the left
        new_row = [i for i in row if i != 0]
        new_row += [0] * (SIZE - len(new_row))
        return new_row

    def merge(self, row):
        # Merge tiles in the row
        for i in range(SIZE - 1):
            if row[i] == row[i + 1] and row[i] != 0:
                row[i] *= 2
                row[i + 1] = 0
                self.score += row[i]
                if row[i] == 2048:
                    self.won = True
        return row

    def move_left(self):
        moved = False
        for i in range(SIZE):
            new_row = self.compress(self.grid[i])
            new_row = self.merge(new_row)
            new_row = self.compress(new_row)
            if self.grid[i] != new_row:
                moved = True
                self.grid[i] = new_row
        return moved

    def move_right(self):
        self.grid = [row[::-1] for row in self.grid]
        moved = self.move_left()
        self.grid = [row[::-1] for row in self.grid]
        return moved

    def move_up(self):
        self.grid = [list(row) for row in zip(*self.grid)]
        moved = self.move_left()
        self.grid = [list(row) for row in zip(*self.grid)]
        return moved

    def move_down(self):
        self.grid = [list(row) for row in zip(*self.grid)]
        moved = self.move_right()
        self.grid = [list(row) for row in zip(*self.grid)]
        return moved

    def can_move(self):
        for i in range(SIZE):
            for j in range(SIZE):
                if self.grid[i][j] == 0:
                    return True
                if i < SIZE - 1 and self.grid[i][j] == self.grid[i + 1][j]:
                    return True
                if j < SIZE - 1 and self.grid[i][j] == self.grid[i][j + 1]:
                    return True
        return False

    def play(self):
        clock = pygame.time.Clock()
        while not self.over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.over = True
                if event.type == pygame.KEYDOWN:
                    moved = False
                    if event.key == pygame.K_LEFT:
                        moved = self.move_left()
                    elif event.key == pygame.K_RIGHT:
                        moved = self.move_right()
                    elif event.key == pygame.K_UP:
                        moved = self.move_up()
                    elif event.key == pygame.K_DOWN:
                        moved = self.move_down()
                    if moved:
                        self.add_new_tile()
                        self.draw_grid()
                        if not self.can_move():
                            self.over = True
                            self.draw_grid()
            clock.tick(10)

if __name__ == '__main__':
    game = Game2048()
    game.play()
    pygame.quit()