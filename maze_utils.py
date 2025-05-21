import random
def load_maze(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    maze = []
    for line in lines:
        row = list(line.strip())  # Convert line into list of characters
        maze.append(row)

    return maze

def get_random_empty_position(maze):
    height = len(maze)
    width = len(maze[0])
    while True:
        x = random.randint(0, width - 1)
        y = random.randint(0, height - 1)
        if maze[y][x] == ' ':
            return (x, y)