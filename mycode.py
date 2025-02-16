import pygame
import random

# Initialize pygame+

pygame.init()

# Constants for the game
SIZE = 4
TILE_SIZE = 150
TILE_MARGIN = 7  
GRID_SIZE = SIZE * (TILE_SIZE + TILE_MARGIN) + TILE_MARGIN  
FONT_SIZE = 50  
SCORE_FONT_SIZE = 30  
BACKGROUND_COLOR = (187, 173, 160)  
TILE_COLORS = {  
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
FONT_COLOR = (119, 110, 101)

# Set up the display
screen = pygame.display.set_mode((GRID_SIZE, GRID_SIZE + 50))
pygame.display.set_caption('2048')

# Load fonts for numbers and score
font = pygame.font.Font(None, FONT_SIZE)
score_font = pygame.font.Font(None, SCORE_FONT_SIZE)

class Game2048:
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        """ Resets the game to start over """
        self.grid = [[0] * SIZE for _ in range(SIZE)]  
        self.score = 0  
        self.over = False  
        self.won = False  
        self.add_new_tile()
        self.add_new_tile()
        self.draw_grid()

    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(SIZE) for j in range(SIZE) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 4 if random.random() >= 0.9 else 2

    def draw_grid(self):
        screen.fill(BACKGROUND_COLOR)  
        for i in range(SIZE):
            for j in range(SIZE):
                value = self.grid[i][j]
                color = TILE_COLORS.get(value, TILE_COLORS[2048])  
                rect = pygame.Rect(
                    TILE_MARGIN + j * (TILE_SIZE + TILE_MARGIN),
                    TILE_MARGIN + i * (TILE_SIZE + TILE_MARGIN) + 50,
                    TILE_SIZE,
                    TILE_SIZE
                )
                pygame.draw.rect(screen, color, rect)  
                if value:
                    text = font.render(str(value), True, FONT_COLOR)  
                    text_rect = text.get_rect(center=rect.center)  
                    screen.blit(text, text_rect)  

        score_text = score_font.render(f'Score: {self.score}', True, FONT_COLOR)
        screen.blit(score_text, (10, 10))
        
        pygame.display.update()  

    def compress(self, row):
        new_row = [i for i in row if i != 0]
        new_row += [0] * (SIZE - len(new_row))
        return new_row

    def merge(self, row):
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

    def game_over_screen(self):
        """ Displays the Game Over screen and waits for user input """
        while True:
            screen.fill(BACKGROUND_COLOR)
            game_over_text = font.render("Game Over!", True, FONT_COLOR)
            score_text = score_font.render(f"Score: {self.score}", True, FONT_COLOR)
            restart_text = score_font.render("Press 'R' to Restart, 'Q' to Quit", True, FONT_COLOR)

            game_over_rect = game_over_text.get_rect(center=(GRID_SIZE // 2, GRID_SIZE // 2 - 50))
            score_rect = score_text.get_rect(center=(GRID_SIZE // 2, GRID_SIZE // 2))
            restart_rect = restart_text.get_rect(center=(GRID_SIZE // 2, GRID_SIZE // 2 + 50))

            screen.blit(game_over_text, game_over_rect)
            screen.blit(score_text, score_rect)
            screen.blit(restart_text, restart_rect)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game()
                        return
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        return

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
                            self.game_over_screen()

            clock.tick(10)

if __name__ == '__main__':
    game = Game2048()
    game.play()
    pygame.quit()
