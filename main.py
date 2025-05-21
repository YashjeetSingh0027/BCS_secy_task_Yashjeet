import pygame
import random
import pickle
import numpy as np
pygame.init()

screen = pygame.display.set_mode((600, 400))
from bfs import bfs
### random movement for harry
def get_random_valid_move(maze, position):
    x, y = position
    valid_moves = []

    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(maze[0]) and 0 <= ny < len(maze):
            if maze[ny][nx] != 'X':
                valid_moves.append((nx, ny))

    if valid_moves:
        return random.choice(valid_moves)
    else:
        return position  ### Stay in place if stuck


from maze_utils import load_maze, get_random_empty_position
maze = load_maze("maze.txt")
harry_pos = get_random_empty_position(maze)
cup_pos = get_random_empty_position(maze)
death_pos = get_random_empty_position(maze)

while cup_pos in [harry_pos, death_pos]:
    cup_pos = get_random_empty_position(maze)

while death_pos in [harry_pos, cup_pos]:
    death_pos = get_random_empty_position(maze)

CELL_SIZE = 40
WALL_COLOR = (50, 50, 50)
EMPTY_COLOR = (255, 255, 255)
HARRY_COLOR = (0, 100, 255)
CUP_COLOR = (255, 215, 0)
DE_COLOR = (200, 0, 0)

ROWS = len(maze)
COLS = len(maze[0])

def draw_maze():
    for y in range(ROWS):
        for x in range(COLS):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

            if (x, y) == harry_pos:
                color = HARRY_COLOR
            elif (x, y) == cup_pos:
                color = CUP_COLOR
            elif (x, y) == death_pos:
                color = DE_COLOR
            elif maze[y][x] == 'X':
                color = WALL_COLOR
            else:
                color = EMPTY_COLOR

            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # Grid lines


clock = pygame.time.Clock()

win = False
game_over = False
run = True
while run:
    screen.fill((0, 0, 0))
    # Draw maze once before loop
    draw_maze()
    pygame.display.update()
    # pygame.time.delay(1000)  # Pause 1 second after pressing run
    clock.tick(3)

    with open("q_table.pkl", "rb") as f:
        Q = pickle.load(f)
    actions = {
        0: (-1, 0),  # LEFT
        1: (1, 0),  # RIGHT
        2: (0, -1),  # UP
        3: (0, 1)  # DOWN
    }
    # ------------- #
    if not game_over:

        state = (harry_pos, death_pos)
        valid_moves = []
        for a, (dx, dy) in actions.items():
            nx, ny = harry_pos[0] + dx, harry_pos[1] + dy
            if 0 <= nx < COLS and 0 <= ny < ROWS and maze[ny][nx] != 'X':
                valid_moves.append((a, (nx, ny)))

        if valid_moves:
            if state in Q:
                # Choose the best valid action from Q-table
                best_action = max(valid_moves, key=lambda x: Q[state][x[0]])
            else:
                # Choose a random valid action
                best_action = random.choice(valid_moves)
            harry_pos = best_action[1]
        # else: harry stays (but this case shouldn't happen if maze is designed right)

        # Move Death Eater toward Harry using BFS
        path = bfs(maze, death_pos, harry_pos)
        if path and len(path) > 1:
            death_pos = path[1]

        # Check for win/loss
        if harry_pos == cup_pos:
            print("Harry reached the Cup!!!")
            game_over = True
            win = True

        elif abs(harry_pos[0] - death_pos[0]) + abs(harry_pos[1] - death_pos[1]) == 1:
            print("Harry is caught!!!")
            game_over = True
            win = False

    # ------------ #
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
pygame.quit()