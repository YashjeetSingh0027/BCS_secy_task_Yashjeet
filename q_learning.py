import random
import numpy as np
from collections import defaultdict
import pickle

from maze_utils import load_maze, get_random_empty_position
from bfs import bfs

# Load maze
maze = load_maze("maze.txt")
ROWS = len(maze)
COLS = len(maze[0])

# Actions: Left, Right, Up, Down
actions = {
    0: (-1, 0),
    1: (1, 0),
    2: (0, -1),
    3: (0, 1)
}

# Q-table: Q[state] = [value for each action]
Q = defaultdict(lambda: np.zeros(4))

# Hyperparameters
alpha = 0.1        # learning rate
gamma = 0.9        # discount factor
epsilon = 1.0        # exploration rate
epsilon_min = 0.01
epsilon_decay = 0.995
episodes = 10000

# Rewards
step_penalty = -1
death_penalty = -100
cup_reward = 150


import matplotlib.pyplot as plt

rewards_per_episode = []
success_count = 0
failure_count = 0
success_rate_list = []
failure_rate_list = []

# Training loop
for ep in range(episodes):
    harry_pos = get_random_empty_position(maze)
    cup_pos = get_random_empty_position(maze)
    death_pos = get_random_empty_position(maze)

    # Ensure unique positions
    while cup_pos in [harry_pos, death_pos]:
        cup_pos = get_random_empty_position(maze)
    while death_pos in [harry_pos, cup_pos]:
        death_pos = get_random_empty_position(maze)

    total_reward = 0
    done = False
    steps = 0

    while not done:
        state = (harry_pos, death_pos)

        # ε-greedy action
        if random.uniform(0, 1) < epsilon:
            action = random.choice(list(actions.keys()))
        else:
            action = np.argmax(Q[state])
        harry_pos_x, harry_pos_y = harry_pos
        dx, dy = actions[action]
        new_x = harry_pos_x + dx
        new_y = harry_pos_y + dy

        # Check bounds and wall
        if 0 <= new_x < COLS and 0 <= new_y < ROWS and maze[new_y][new_x] != 'X':
            harry_pos = (new_x, new_y)

        # Move Death Eater
        path = bfs(maze, death_pos, harry_pos)
        if path and len(path) > 1:
            death_pos = path[1]

        # Reward logic
        if harry_pos == death_pos:
            reward = death_penalty
            done = True
        elif harry_pos == cup_pos:
            reward = cup_reward
            done = True
        else:
            reward = step_penalty
        # Manhattan distances
        old_dist_to_cup = abs(state[0][0] - cup_pos[0]) + abs(state[0][1] - cup_pos[1])
        new_dist_to_cup = abs(harry_pos[0] - cup_pos[0]) + abs(harry_pos[1] - cup_pos[1])

        old_dist_to_death = abs(state[0][0] - state[1][0]) + abs(state[0][1] - state[1][1])
        new_dist_to_death = abs(harry_pos[0] - death_pos[0]) + abs(harry_pos[1] - death_pos[1])

        # Add shaping rewards
        delta_cup = old_dist_to_cup - new_dist_to_cup
        delta_death = new_dist_to_death - old_dist_to_death

        reward += 0.5 * delta_cup  # reward getting closer to cup
        reward += 0.1 * delta_death  # reward getting farther from Death Eater
        next_state = (harry_pos, death_pos)
        Q[state][action] += alpha * (reward + gamma * np.max(Q[next_state]) - Q[state][action])
        total_reward += reward
        steps += 1

        if steps > 100:  #
            done = True
    if harry_pos == cup_pos:
        success_count += 1
    elif harry_pos == death_pos:
        failure_count += 1

    rewards_per_episode.append(total_reward)
    success_rate = success_count / (ep + 1)
    failure_rate = failure_count / (ep + 1)
    success_rate_list.append(success_rate)
    failure_rate_list.append(failure_rate)

    print(
        f"Episode {ep + 1}/{episodes} | Reward: {total_reward:.2f} | Success: {success_rate:.2%} | Failure: {failure_rate:.2%} | ε: {epsilon:.4f}")
    epsilon = max(epsilon_min, epsilon * epsilon_decay)

    print(f"Episode Number {(ep + 1)}/{episodes} | Total reward: {round(total_reward)} | ε: {round(epsilon,2)}")

# Save the Q-table
with open("q_table.pkl", "wb") as f:
    pickle.dump(dict(Q), f)

# Plotting learning curves
plt.figure(figsize=(12, 6))

# Reward curve
plt.subplot(1, 2, 1)
plt.plot(rewards_per_episode, label="Total Reward per Episode", color='blue', alpha=0.6)
plt.xlabel("Episode")
plt.ylabel("Reward")
plt.title("Reward Curve")
plt.grid(True)
plt.legend()

# Success/failure rate
plt.subplot(1, 2, 2)
plt.plot(success_rate_list, label="Success Rate", color='green')
plt.plot(failure_rate_list, label="Failure Rate", color='red')
plt.xlabel("Episode")
plt.ylabel("Rate")
plt.title("Success vs Failure Rate")
plt.grid(True)
plt.legend()

plt.tight_layout()
plt.savefig("learning_curves.png")
plt.show()
print("Training complete. Q-table saved as q_table.pkl ✅")