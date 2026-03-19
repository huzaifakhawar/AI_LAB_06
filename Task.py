import heapq
from collections import deque
import time
from copy import deepcopy

class PuzzleState:
    """Represents a state of the 8-puzzle"""
    
    def __init__(self, grid, parent=None, move="Start", g_cost=0):
        """
        Initialize a puzzle state
        grid: 3x3 2D list representing the puzzle
        parent: parent state for path tracking
        move: the move taken to reach this state
        g_cost: cost from start node
        """
        self.grid = [row[:] for row in grid]  # Deep copy
        self.parent = parent
        self.move = move
        self.g_cost = g_cost
        
        # Find position of blank (0)
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] == 0:
                    self.blank_row, self.blank_col = i, j
                    break
    
    def __hash__(self):
        """Make state hashable for visited set"""
        return hash(tuple(tuple(row) for row in self.grid))
    
    def __eq__(self, other):
        """Check equality of two states"""
        return self.grid == other.grid
    
    def __lt__(self, other):
        """Comparison for priority queue (f_cost)"""
        return self.f_cost < other.f_cost
    
    def is_goal(self, goal_grid):
        """Check if current state is goal state"""
        return self.grid == goal_grid
    
    def get_manhattan_distance(self, goal_grid):
        """
        Heuristic function: Manhattan distance
        Sum of distances from each tile to its goal position
        """
        distance = 0
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] != 0:  # Skip blank tile
                    value = self.grid[i][j]
                    # Find goal position of this value
                    for goal_i in range(3):
                        for goal_j in range(3):
                            if goal_grid[goal_i][goal_j] == value:
                                distance += abs(i - goal_i) + abs(j - goal_j)
                                break
        return distance
    
    def get_misplaced_tiles(self, goal_grid):
        """
        Alternative heuristic: Count misplaced tiles
        """
        count = 0
        for i in range(3):
            for j in range(3):
                if self.grid[i][j] != 0 and self.grid[i][j] != goal_grid[i][j]:
                    count += 1
        return count
    
    def get_successors(self):
        """
        Generate all valid successor states (children)
        Blank can move: up, down, left, right
        """
        successors = []
        directions = [
            (-1, 0, "Up"),      # Move up
            (1, 0, "Down"),     # Move down
            (0, -1, "Left"),    # Move left
            (0, 1, "Right")     # Move right
        ]
        
        for di, dj, direction in directions:
            new_row = self.blank_row + di
            new_col = self.blank_col + dj
            
            # Check if new position is within bounds
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                # Create new state by swapping blank with adjacent tile
                new_grid = [row[:] for row in self.grid]
                new_grid[self.blank_row][self.blank_col], new_grid[new_row][new_col] = \
                    new_grid[new_row][new_col], new_grid[self.blank_row][self.blank_col]
                
                new_state = PuzzleState(
                    new_grid,
                    parent=self,
                    move=direction,
                    g_cost=self.g_cost + 1
                )
                successors.append(new_state)
        
        return successors
    
    def display(self):
        """Display the puzzle grid"""
        for row in self.grid:
            print(row)
        print()


class AStar8PuzzleAgent:
    """Goal-based intelligent agent using A* algorithm for 8-puzzle"""
    
    def __init__(self, initial_grid, goal_grid, heuristic="manhattan"):
        """
        Initialize the agent
        initial_grid: starting puzzle configuration
        goal_grid: target puzzle configuration
        heuristic: "manhattan" or "misplaced"
        """
        self.initial_state = PuzzleState(initial_grid)
        self.goal_grid = goal_grid
        self.heuristic_type = heuristic
        self.solution_path = []
        self.visited_states = set()
        self.explored_count = 0
        self.generated_count = 0
    
    def calculate_heuristic(self, state):
        """Calculate heuristic value for a state"""
        if self.heuristic_type == "manhattan":
            return state.get_manhattan_distance(self.goal_grid)
        else:
            return state.get_misplaced_tiles(self.goal_grid)
    
    def solve(self):
        """
        Solve the 8-puzzle using A* algorithm
        Returns: True if solution found, False otherwise
        """
        print("=" * 60)
        print("🤖 A* ALGORITHM FOR 8-PUZZLE PROBLEM")
        print("=" * 60)
        print(f"\n📋 Initial State:")
        self.initial_state.display()
        
        print(f"🎯 Goal State:")
        for row in self.goal_grid:
            print(row)
        print()
        
        print(f"📊 Using Heuristic: {self.heuristic_type.upper()}")
        print(f"Evaluation Function: f(n) = g(n) + h(n)")
        print("-" * 60)
        
        # Priority queue: (f_cost, counter, state)
        # counter ensures FIFO order for states with same f_cost
        open_list = []
        counter = 0
        
        # Calculate h and f for initial state
        self.initial_state.h_cost = self.calculate_heuristic(self.initial_state)
        self.initial_state.f_cost = self.initial_state.g_cost + self.initial_state.h_cost
        
        heapq.heappush(open_list, (self.initial_state.f_cost, counter, self.initial_state))
        self.generated_count = 1
        
        start_time = time.time()
        
        while open_list:
            # Get state with minimum f_cost
            _, _, current_state = heapq.heappop(open_list)
            
            # Avoid revisiting states
            state_hash = hash(current_state)
            if state_hash in self.visited_states:
                continue
            
            self.visited_states.add(state_hash)
            self.explored_count += 1
            
            # Check if goal state is reached
            if current_state.is_goal(self.goal_grid):
                elapsed_time = time.time() - start_time
                self._extract_solution_path(current_state)
                self._display_solution(elapsed_time)
                return True
            
            # Expand current state: generate successors
            successors = current_state.get_successors()
            
            for successor in successors:
                if hash(successor) not in self.visited_states:
                    # Calculate h and f for successor
                    successor.h_cost = self.calculate_heuristic(successor)
                    successor.f_cost = successor.g_cost + successor.h_cost
                    
                    heapq.heappush(open_list, (successor.f_cost, counter, successor))
                    self.generated_count += 1
                    counter += 1
        
        print("\n❌ No solution found!")
        return False
    
    def _extract_solution_path(self, goal_state):
        """Backtrack from goal state to extract solution path"""
        current = goal_state
        while current is not None:
            self.solution_path.append(current)
            current = current.parent
        self.solution_path.reverse()
    
    def _display_solution(self, elapsed_time):
        """Display the complete solution with analysis"""
        print("\n" + "=" * 60)
        print("✅ SOLUTION FOUND!")
        print("=" * 60)
        
        print(f"\n📈 Agent Decision-Making Analysis:")
        print(f"   • States Explored: {self.explored_count}")
        print(f"   • States Generated: {self.generated_count}")
        print(f"   • Time Taken: {elapsed_time:.4f} seconds")
        print(f"   • Optimal Solution Length: {len(self.solution_path) - 1} moves")
        
        print(f"\n🔍 Complete Solution Path:")
        print("-" * 60)
        
        for idx, state in enumerate(self.solution_path):
            print(f"\nStep {idx}: {state.move}")
            if idx > 0:
                print(f"  g(n) = {state.g_cost} (cost from start)")
                print(f"  h(n) = {state.h_cost} ({self.heuristic_type} distance)")
                print(f"  f(n) = {state.f_cost} (total evaluation)")
            else:
                print(f"  [Initial State]")
            
            state.display()
        
        print("=" * 60)
        print(f"🎯 FINAL RESULT:")
        print(f"   • Sequence of Moves: {' → '.join([s.move for s in self.solution_path[1:]])}")
        print(f"   • Total Cost (Moves): {len(self.solution_path) - 1}")
        print("=" * 60)


def main():
    """Main function to demonstrate the 8-puzzle agent"""
    
    # Example: Initial puzzle configuration
    # 0 represents blank space
    initial_state = [
        [1, 2, 3],
        [4, 0, 5],
        [7, 8, 6]
    ]
    
    # Goal configuration
    goal_state = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]
    
    # Create and run agent
    agent = AStar8PuzzleAgent(initial_state, goal_state, heuristic="manhattan")
    agent.solve()
    
    print("\n" + "=" * 60)
    print("📝 EXPLANATION OF OPTIMAL DECISION-MAKING:")
    print("=" * 60)
    print("""
The A* algorithm ensures optimal decision-making through:

1. **Informed Search Strategy**:
   - Uses heuristic function h(n) to estimate distance to goal
   - Evaluates states based on f(n) = g(n) + h(n)
   - Prioritizes states with lower f(n) values

2. **Cost Awareness (g(n))**:
   - Tracks actual cost from start node
   - Ensures we follow lowest-cost paths
   - Prevents unnecessary exploration

3. **Goal Estimation (h(n))**:
   - Manhattan Distance: Sum of moves each tile needs
   - Provides good estimate of remaining distance
   - Allows early pruning of non-promising paths

4. **Optimality Guarantee**:
   - A* finds shortest path when h(n) is admissible
   - Never underestimates distance to goal
   - Explores fewer nodes than uninformed search

5. **State Space Exploration**:
   - Open list maintains promising states sorted by f(n)
   - Visited set prevents revisiting states
   - Successor generation creates valid moves only
    """)


if __name__ == "__main__":
    main()
