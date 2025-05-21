# BCS_secy_task_Yashjeet
Yashjeet's submission for BCS secretary recruitment task

---

Basic Approach

1. Maze Environment: Grid world with walls (`'X'`) and empty spaces.
2. Agent (Harry Potter) Learns via **Q-Learning** to reach the Cup.
3. Enemy (Death Eater): Moves using **BFS** towards Harry in each step.
4. Reward System:
   - Reaching the Cup: +150
   - Getting caught: -100
   - Each move: -1 step penalty
   - Distance shaping rewards to guide learning
5. Game Ends If:
   - Harry reaches the cup
   - Death Eater reaches Harry or an adjacent cell
   - 200 steps are exceeded (timeout)

---

## 🛠️ Assumptions

- The Death Eater uses the shortest path (BFS) toward Harry.
- Harry always takes an action each frame and is never idle.
- Game ends if Death Eater is **adjacent to** Harry (custom logic applied).

---

 How to train
 
-- just run the q_learning.py file. it will create a q_table.pkl file. and our character will move accordingly...
