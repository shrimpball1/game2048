import pygame
import random

pygame.init()

GRID_SIZE = 4
TILE_SIZE = 100
GRID_MARGIN = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FONT_SIZE = 36
BUTTON_FONT_SIZE = 24

size = (GRID_SIZE * TILE_SIZE + (GRID_SIZE + 1) * GRID_MARGIN, GRID_SIZE * TILE_SIZE + (GRID_SIZE + 1) * GRID_MARGIN + 100)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("2048 Game")

tile_colors = {
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
    2048: (237, 194, 46),
}

font = pygame.font.Font(None, FONT_SIZE)
button_font = pygame.font.Font(None, BUTTON_FONT_SIZE)

grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]

def add_new_tile():
    empty_cells = [(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE) if grid[x][y] == 0]
    if empty_cells:
        x, y = random.choice(empty_cells)
        grid[x][y] = random.choice([2, 4])

def draw_grid():
    screen.fill(BLACK)
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            value = grid[x][y]
            color = tile_colors.get(value, tile_colors[0])
            pygame.draw.rect(
                screen,
                color,
                (y * TILE_SIZE + (y + 1) * GRID_MARGIN, x * TILE_SIZE + (x + 1) * GRID_MARGIN, TILE_SIZE, TILE_SIZE)
            )
            if value != 0:
                text = font.render(str(value), True, BLACK if value < 128 else WHITE)
                text_rect = text.get_rect(center=(y * TILE_SIZE + (y + 1) * GRID_MARGIN + TILE_SIZE / 2, x * TILE_SIZE + (x + 1) * GRID_MARGIN + TILE_SIZE / 2))
                screen.blit(text, text_rect)

def move(direction):
    moved = False
    if direction == 'LEFT':
        for row in range(GRID_SIZE):
            for col in range(1, GRID_SIZE):
                if grid[row][col] != 0:
                    for k in range(col, 0, -1):
                        if grid[row][k - 1] == 0:
                            grid[row][k - 1], grid[row][k] = grid[row][k], grid[row][k - 1]
                            moved = True
                        elif grid[row][k - 1] == grid[row][k]:
                            grid[row][k - 1] *= 2
                            grid[row][k] = 0
                            moved = True
                            break
                        elif grid[row][k - 1] != grid[row][k]:
                            break
    elif direction == 'RIGHT':
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE - 2, -1, -1):
                if grid[row][col] != 0:
                    for k in range(col, GRID_SIZE - 1):
                        if grid[row][k + 1] == 0:
                            grid[row][k + 1], grid[row][k] = grid[row][k], grid[row][k + 1]
                            moved = True
                        elif grid[row][k + 1] == grid[row][k]:
                            grid[row][k + 1] *= 2
                            grid[row][k] = 0
                            moved = True
                            break
                        elif grid[row][k + 1] != grid[row][k]:
                            break
    elif direction == 'UP':
        for col in range(GRID_SIZE):
            for row in range(1, GRID_SIZE):
                if grid[row][col] != 0:
                    for k in range(row, 0, -1):
                        if grid[k - 1][col] == 0:
                            grid[k - 1][col], grid[k][col] = grid[k][col], grid[k - 1][col]
                            moved = True
                        elif grid[k - 1][col] == grid[k][col]:
                            grid[k - 1][col] *= 2
                            grid[k][col] = 0
                            moved = True
                            break
                        elif grid[k - 1][col] != grid[k][col]:
                            break
    elif direction == 'DOWN':
        for col in range(GRID_SIZE):
            for row in range(GRID_SIZE - 2, -1, -1):
                if grid[row][col] != 0:
                    for k in range(row, GRID_SIZE - 1):
                        if grid[k + 1][col] == 0:
                            grid[k + 1][col], grid[row][col] = grid[row][col], grid[k + 1][col]
                            moved = True
                        elif grid[k + 1][col] == grid[row][col]:
                            grid[k + 1][col] *= 2
                            grid[row][col] = 0
                            moved = True
                            break
                        elif grid[k + 1][col] != grid[row][col]:
                            break
    return moved

def can_move():              # to find space to add new 2 or 4 and make the same numbers add together
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] == 0:
                return True
            if col < GRID_SIZE - 1 and grid[row][col] == grid[row][col + 1]:
                return True
            if row < GRID_SIZE - 1 and grid[row][col] == grid[row + 1][col]:
                return True
    return False

def has_won():                 # get 2048 and end the game 
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if grid[row][col] == 2048:
                return True
    return False

def reset_game():               # reset game after game over
    global grid
    grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    add_new_tile()
    add_new_tile()

def draw_end_screen(message):    # screen after game over
    screen.fill(BLACK)
    text = font.render(message, True, WHITE)
    text_rect = text.get_rect(center=(size[0] // 2, size[1] // 2 - 50))
    screen.blit(text, text_rect)
    
    button_rect = pygame.Rect(size[0] // 2 - 50, size[1] // 2, 100, 50)
    pygame.draw.rect(screen, RED, button_rect)
    button_text = button_font.render("Try Again", True, WHITE)
    button_text_rect = button_text.get_rect(center=button_rect.center)
    screen.blit(button_text, button_text_rect)
    
    pygame.display.flip()
    
    return button_rect

running = True
game_over = False
add_new_tile()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and not game_over:
            moved = False
            if event.key == pygame.K_LEFT:
                moved = move('LEFT')
            elif event.key == pygame.K_RIGHT:
                moved = move('RIGHT')
            elif event.key == pygame.K_UP:
                moved = move('UP')
            elif event.key == pygame.K_DOWN:
                moved = move('DOWN')
            if moved:
                add_new_tile()
                if has_won():
                    game_over = True
                    button_rect = draw_end_screen("You Win!")
                elif not can_move():
                    game_over = True
                    button_rect = draw_end_screen("You Lose")
        elif event.type == pygame.MOUSEBUTTONDOWN and game_over:
            if button_rect.collidepoint(event.pos):
                game_over = False
                reset_game()
    
    if not game_over:
        draw_grid()
        pygame.display.flip()

pygame.quit()
