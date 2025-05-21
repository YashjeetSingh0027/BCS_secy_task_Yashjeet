from collections import deque

def bfs(maze, start, goal):

    queue = deque()
    visited = set()
    parent = {}

    queue.append(start)
    visited.add(start)

    while queue:
        current = queue.popleft()

        if current == goal:
            break

        x, y = current
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Left, Right, Up, Down
            nx, ny = x + dx, y + dy

            if 0 <= nx < len(maze[0]) and 0 <= ny < len(maze):
                if maze[ny][nx] != 'X' and (nx, ny) not in visited:
                    queue.append((nx, ny))
                    visited.add((nx, ny))
                    parent[(nx, ny)] = (x, y)
    path = []
    current = goal
    while current != start:
        path.append(current)
        if current in parent:
            current = parent[current]
        else:
            return None  # No path found

    path.append(start)
    path.reverse()
    return path