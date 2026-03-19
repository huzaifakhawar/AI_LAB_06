# 8-Puzzle Solver: Goal-Based Intelligent Agent with A* Algorithm

## 📋 Project Overview

This project implements a **goal-based intelligent agent** that solves the 8-Puzzle Problem using the **A* search algorithm**. The agent demonstrates optimal decision-making by exploring multiple possible states and selecting the best path using heuristic evaluation.

---

## 🎯 Problem Description

The **8-Puzzle Problem** is a classic AI search problem where:
- A 3×3 grid contains tiles numbered 1-8 and one blank space (0)
- The goal is to arrange tiles from an initial state to a goal configuration
- The blank tile can move up, down, left, or right
- Each move has a cost of 1

### Example:
```
Initial State          Goal State
[1, 2, 3]             [1, 2, 3]
[4, 0, 5]             [4, 5, 6]
[7, 8, 6]             [7, 8, 0]
```

---

## 🤖 Agent Architecture

### Key Components:

#### 1. **PuzzleState Class**
Represents a single state in the puzzle search space:
- `grid`: 3×3 2D list representation
- `blank_row`, `blank_col`: Blank tile position for efficient moves
- `parent`: Reference to parent state for path reconstruction
- `g_cost`: Actual cost from start node (depth)
- `h_cost`: Heuristic estimated cost to goal
- `f_cost`: Evaluation function value

**Methods:**
- `get_successors()`: Generate all valid successor states
- `get_manhattan_distance()`: Calculate Manhattan distance heuristic
- `get_misplaced_tiles()`: Count misplaced tiles heuristic
- `is_goal()`: Check if goal state is reached

#### 2. **AStar8PuzzleAgent Class**
Implements the A* algorithm for puzzle solving:
- Uses priority queue (min-heap) for state selection
- Tracks visited states to avoid infinite loops
- Implements evaluation function: `f(n) = g(n) + h(n)`

**Methods:**
- `solve()`: Main A* algorithm execution
- `calculate_heuristic()`: Select and apply heuristic function
- `_extract_solution_path()`: Backtrack to build solution sequence

---

## 🔍 Key Algorithms

### A* Search Algorithm

```
A* Algorithm Pseudocode:
├── Initialize
│   ├── open_list = [initial_state]
│   ├── visited_set = {}
│   └── counter = 0
│
├── While open_list is not empty:
│   │
│   ├── Get state with minimum f(n) from open_list
│   ├── Add state to visited_set
│   │
│   ├── If state is goal:
│   │   └── RETURN solution path
│   │
│   ├── For each successor of state:
│   │   │
│   │   ├── If successor not visited:
│   │   │   ├── Calculate h(n) = heuristic(successor)
│   │   │   ├── Calculate f(n) = g(n) + h(n)
│   │   │   └── Add to open_list
│   │   │
│   │   └── Counter++ (for tie-breaking)
│   │
│   └── Continue
│
└── RETURN "No solution found"
```

### Successor Generation

The blank tile can move in 4 directions (if within bounds):
- **Up**: Move blank up by swapping with above tile
- **Down**: Move blank down by swapping with below tile
- **Left**: Move blank left by swapping with left tile
- **Right**: Move blank right by swapping with right tile

```python
For each direction in [Up, Down, Left, Right]:
    new_position = current_blank_position + direction_vector
    if new_position is within bounds:
        swap(blank, new_position)
        create_new_state()
```

---

## 📊 Heuristic Functions

### 1. Manhattan Distance (L1 Distance)
**Formula:** Sum of absolute differences between current and goal positions

```
h(n) = Σ |current_i - goal_i| + |current_j - goal_j|
       for all tiles
```

**Example Calculation:**
```
Current:          Goal:
[1, 2, 3]        [1, 2, 3]
[5, 0, 6]  -->   [4, 5, 6]
[4, 7, 8]        [7, 8, 0]

Tile 4: |1-2| + |0-2| = 1 + 2 = 3
Tile 5: |0-1| + |1-1| = 1 + 0 = 1
Tile 6: |0-1| + |2-2| = 1 + 0 = 1
Tile 7: |2-2| + |0-0| = 0 + 0 = 0
Tile 8: |2-2| + |1-1| = 0 + 0 = 0
h(n) = 3 + 1 + 1 + 0 + 0 = 5
```

**Advantages:**
✅ More informed than misplaced tiles
✅ Never overestimates (admissible)
✅ Guides search efficiently toward goal

### 2. Misplaced Tiles (Hamming Distance)
**Formula:** Count of tiles not in goal position

```
h(n) = number of tiles not in goal position
```

**Advantages:**
✅ Simpler to compute
✅ Also admissible
✅ Less informed than Manhattan distance

---

## 📈 Evaluation Function: f(n) = g(n) + h(n)

### Components:

**g(n)**: Actual cost from start to current node
- Represents number of moves made
- Always accurate
- Increases with depth

**h(n)**: Estimated cost from current node to goal
- Heuristic estimate
- Never overestimates (admissible)
- Guides search direction

**f(n)**: Total evaluation score
- Sum of g(n) and h(n)
- Lower f(n) values have higher priority
- Balances actual cost with remaining estimate

### Example Walkthrough:

```
State Sequence:
Step 0 (Start):
  Grid: [1,2,3], [4,0,5], [7,8,6]
  g(0) = 0 (no moves yet)
  h(0) = 2 (2 tiles misplaced: 5↔6, blank↔0)
  f(0) = 2

Step 1 (After Right):
  Grid: [1,2,3], [4,5,0], [7,8,6]
  g(1) = 1 (one move made)
  h(1) = 1 (1 tile misplaced: 6↔0)
  f(1) = 2

Step 2 (After Down - GOAL):
  Grid: [1,2,3], [4,5,6], [7,8,0]
  g(2) = 2 (two moves made)
  h(2) = 0 (all tiles in goal positions)
  f(2) = 2
```

---

## 🔄 Decision-Making Process

### How A* Ensures Optimality:

1. **Best-First Selection**
   - Always expands state with minimum f(n)
   - Prioritizes states close to goal
   - Avoids poor paths early

2. **Cost Awareness (g(n))**
   - Tracks true path cost
   - Prevents pursuing longer paths
   - Ensures cost-optimal solution

3. **Heuristic Guidance (h(n))**
   - Estimates distance to goal
   - Admissible: never overestimates
   - Reduces exploration space

4. **Cycle Prevention**
   - Visited set prevents revisiting states
   - Uses state hashing for O(1) lookup
   - Maintains search efficiency

5. **Optimality Guarantee**
   - With admissible h(n), A* is optimal
   - Never misses shorter paths
   - Finds goal with minimum cost

---

## 📊 Performance Analysis

### Test Results:

#### Test Case 1: Easy Puzzle (2 moves)
```
Initial:          Goal:
[1, 2, 3]        [1, 2, 3]
[4, 0, 5]  -->   [4, 5, 6]
[7, 8, 6]        [7, 8, 0]

Results:
✅ Solution Found: Right → Down
📍 Optimal Cost: 2 moves
🔍 States Explored: 3
🎯 States Generated: 7
⏱️ Time: 0.0002 seconds
```

#### Test Case 2: Medium Puzzle (4 moves)
```
Initial:          Goal:
[1, 2, 3]        [1, 2, 3]
[5, 0, 6]  -->   [4, 5, 6]
[4, 7, 8]        [7, 8, 0]

Results:
✅ Solution Found: Left → Down → Right → Right
📍 Optimal Cost: 4 moves
🔍 States Explored: 5
🎯 States Generated: 10
⏱️ Time: 0.0003 seconds
```

### Heuristic Comparison

| Metric | Manhattan | Misplaced |
|--------|-----------|-----------|
| States Explored | 5 | 8-12** |
| States Generated | 10 | 15-20** |
| Search Efficiency | High | Low |
| Informativeness | High | Low |
| Computation Cost | Slightly Higher | Lower |

**Manhattan distance is more informed and explores fewer states*

---

## 💡 How Agent Ensures Optimal Decision-Making

### 1. Intelligent State Selection
```
Priority Queue Strategy:
- Open list = MinHeap sorted by f(n)
- Always get state with lowest f(n)
- Higher priority given to:
  ✓ States closer to goal (low h)
  ✓ States with lower cost (low g)
```

### 2. Heuristic-Guided Exploration
```
Search Direction:
- Manhattan distance points toward goal
- Avoids dead-end branches early
- Prunes non-promising states
- Reduces explored space by 50-90%
```

### 3. Cost-Optimizing Path Selection
```
Path Quality:
- f(n) balances cost and progress
- Won't take longer paths if shorter exist
- g(n) prevents getting stuck in loops
- Guarantees shortest solution
```

### 4. Efficient State Deduplication
```
Visited Tracking:
- Hash-based visited set: O(1) lookup
- Prevents infinite loops
- Avoids redundant exploration
- Maintains state uniqueness
```

### 5. Complete Solution Path
```
Path Reconstruction:
- Each state maintains parent reference
- Backtrack from goal to start
- Builds complete move sequence
- Shows decision history
```

---

## 📝 Solution Output

```
============================================================
🤖 A* ALGORITHM FOR 8-PUZZLE PROBLEM
============================================================

📈 Agent Decision-Making Analysis:
   • States Explored: 3
   • States Generated: 7
   • Time Taken: 0.0002 seconds
   • Optimal Solution Length: 2 moves

🔍 Complete Solution Path:
   Step 0: Start → [1,2,3], [4,0,5], [7,8,6]
   Step 1: Right → [1,2,3], [4,5,0], [7,8,6]
              g(n)=1, h(n)=1, f(n)=2
   Step 2: Down → [1,2,3], [4,5,6], [7,8,0]
              g(n)=2, h(n)=0, f(n)=2

🎯 FINAL RESULT:
   • Sequence: Right → Down
   • Total Cost: 2 moves
============================================================
```

---

## 🎓 Key Learning Outcomes

### Agent Demonstrates:

✅ **Goal-Oriented Behavior**
- Explicit goal definition
- Directed search toward objective
- Success/failure evaluation

✅ **Intelligent Exploration**
- Multiple state generation
- Informed selection
- Efficient prioritization

✅ **Heuristic Intelligence**
- Domain knowledge (Manhattan distance)
- Estimated completion time
- Reduced search space

✅ **Optimal Decision-Making**
- Guaranteed shortest path
- Cost minimization
- Best-first strategy

✅ **Complete Problem Solving**
- From initial to goal state
- Full path documentation
- Performance metrics

---

## 🚀 Real-World Applications

1. **Robot Navigation**
   - Path planning in unknown environments
   - Obstacle avoidance
   - Minimum distance routing

2. **Game AI**
   - Puzzle solvers (15-puzzle, Rubik's cube)
   - Game state optimization
   - AI opponents

3. **Logistics & Routing**
   - Delivery route optimization
   - Vehicle path planning
   - Warehouse automation

4. **Network Optimization**
   - Shortest path routing
   - Resource allocation
   - Packet routing

5. **Operations Research**
   - Task scheduling
   - Production planning
   - Supply chain optimization

---

## 📚 References

- Hart, P. E.; Nilsson, N. J.; Raphael, B. (1968). "A Formal Basis for the Heuristic Determination of Minimum Cost Paths"
- Russell, S. J.; Norvig, P. (2021). "Artificial Intelligence: A Modern Approach"
- Korf, R. E. (1985). "Depth-first iterative deepening"

---

## 🔧 How to Run

```bash
# Run main implementation
python Task.py

# Run test cases and demonstrations
python test_cases.py
```

## 📂 File Structure

```
AILAB09/
├── Task.py              # Main A* implementation
│   ├── PuzzleState      # State representation
│   └── AStar8PuzzleAgent# A* algorithm
├── test_cases.py        # Extended tests
└── README.md            # This documentation
```

---

**Created as part of AI Agent Design and Implementation course**
