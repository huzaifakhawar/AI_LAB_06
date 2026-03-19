"""
Extended test cases and demonstrations for the A* 8-Puzzle Agent
Shows different puzzle difficulties and heuristic comparisons
"""

from Task import AStar8PuzzleAgent, PuzzleState

def test_case_1():
    """Easy puzzle - 2 moves"""
    print("\n" + "🎯" * 30)
    print("TEST CASE 1: EASY PUZZLE (2 moves)")
    print("🎯" * 30)
    
    initial = [
        [1, 2, 3],
        [4, 0, 5],
        [7, 8, 6]
    ]
    
    goal = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]
    
    agent = AStar8PuzzleAgent(initial, goal, heuristic="manhattan")
    agent.solve()


def test_case_2():
    """Medium puzzle - 4 moves"""
    print("\n" + "🎯" * 30)
    print("TEST CASE 2: MEDIUM PUZZLE (4 moves)")
    print("🎯" * 30)
    
    initial = [
        [1, 2, 3],
        [5, 0, 6],
        [4, 7, 8]
    ]
    
    goal = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]
    
    agent = AStar8PuzzleAgent(initial, goal, heuristic="manhattan")
    agent.solve()


def test_case_3():
    """Harder puzzle - more moves"""
    print("\n" + "🎯" * 30)
    print("TEST CASE 3: HARDER PUZZLE")
    print("🎯" * 30)
    
    initial = [
        [2, 1, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]
    
    goal = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]
    
    agent = AStar8PuzzleAgent(initial, goal, heuristic="manhattan")
    agent.solve()


def compare_heuristics():
    """Compare Manhattan distance vs Misplaced tiles heuristics"""
    print("\n" + "=" * 60)
    print("HEURISTIC COMPARISON")
    print("=" * 60)
    
    initial = [
        [1, 2, 3],
        [5, 0, 6],
        [4, 7, 8]
    ]
    
    goal = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]
    
    print("\n📊 Using MANHATTAN DISTANCE Heuristic:")
    print("-" * 60)
    agent_manhattan = AStar8PuzzleAgent(initial, goal, heuristic="manhattan")
    agent_manhattan.solve()
    
    print("\n📊 Using MISPLACED TILES Heuristic:")
    print("-" * 60)
    agent_misplaced = AStar8PuzzleAgent(initial, goal, heuristic="misplaced")
    agent_misplaced.solve()
    
    print("\n" + "=" * 60)
    print("COMPARISON RESULTS:")
    print("=" * 60)
    print(f"Manhattan Distance:")
    print(f"  - States Explored: {agent_manhattan.explored_count}")
    print(f"  - States Generated: {agent_manhattan.generated_count}")
    print(f"\nMisplaced Tiles:")
    print(f"  - States Explored: {agent_misplaced.explored_count}")
    print(f"  - States Generated: {agent_misplaced.generated_count}")
    print(f"\n✨ Manhattan Distance explores fewer states (better informed)")


def analyze_successor_generation():
    """Demonstrate successor state generation"""
    print("\n" + "=" * 60)
    print("SUCCESSOR STATE GENERATION ANALYSIS")
    print("=" * 60)
    
    state = PuzzleState([
        [1, 2, 3],
        [4, 0, 5],
        [7, 8, 6]
    ])
    
    print("\n📍 Initial State:")
    state.display()
    
    print("🔄 Generated Successors (All Valid Moves):")
    successors = state.get_successors()
    
    for i, successor in enumerate(successors, 1):
        print(f"\nMove {i}: {successor.move}")
        successor.display()
    
    print(f"✅ Total Valid Moves Generated: {len(successors)}")
    print(f"📌 Blank Position: Row {state.blank_row}, Col {state.blank_col}")


def demonstrate_evaluation_function():
    """Show evaluation function examples"""
    print("\n" + "=" * 60)
    print("EVALUATION FUNCTION DEMONSTRATION: f(n) = g(n) + h(n)")
    print("=" * 60)
    
    goal = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]
    
    # Example states at different depths
    states = [
        ([1, 2, 3], [4, 0, 5], [7, 8, 6], 0, "Start"),
        ([1, 2, 3], [4, 5, 0], [7, 8, 6], 1, "After 1 move"),
        ([1, 2, 3], [0, 5, 4], [7, 8, 6], 2, "After 2 moves"),
    ]
    
    print("\n📋 State Evaluations:")
    print("-" * 60)
    
    for grid_rows, g_cost, label in [
        ((1, 2, 3), (4, 0, 5), (7, 8, 6), 0, "Initial"),
        ((1, 2, 3), (4, 5, 0), (7, 8, 6), 1, "After 1 move"),
        ((1, 2, 3), (4, 5, 6), (7, 8, 0), 2, "Goal state"),
    ]:
        grid = [list(grid_rows[0:3]), list(grid_rows[3:6]) if len(grid_rows) > 3 else [4, 0, 5],
                list(grid_rows[6:9]) if len(grid_rows) > 6 else [7, 8, 6]]
        state = PuzzleState(grid, None, label, g_cost)
        h = state.get_manhattan_distance(goal)
        f = state.g_cost + h
        
        print(f"\n{label}:")
        print(f"  g(n) = {state.g_cost} (actual cost from start)")
        print(f"  h(n) = {h} (estimated distance to goal - Manhattan)")
        print(f"  f(n) = {f} (total evaluation score)")
        print(f"  Priority: {'⭐' * (5 - f)} (lower is better)")


if __name__ == "__main__":
    
    # Run all demonstrations
    test_case_1()
    test_case_2()
    test_case_3()
    
    compare_heuristics()
    
    analyze_successor_generation()
    
    demonstrate_evaluation_function()
    
    # Final summary
    print("\n" + "=" * 60)
    print("🎓 AGENT LEARNING OUTCOMES")
    print("=" * 60)
    print("""
The A* 8-Puzzle Agent demonstrates:

1. ✅ PROBLEM REPRESENTATION
   - States represented as 3x3 grids
   - Blank position tracked for efficient moves
   - Parent pointers for path reconstruction

2. ✅ SUCCESSOR GENERATION
   - All valid moves (4 directions max)
   - Boundary checking to prevent invalid states
   - Each successor tracked with: move, parent, cost

3. ✅ HEURISTIC FUNCTIONS
   - Manhattan Distance: sum of tile distance to goal
   - Misplaced Tiles: count of wrongly placed tiles
   - Both are admissible (never overestimate)

4. ✅ EVALUATION FUNCTION
   - f(n) = g(n) + h(n)
   - g(n): actual cost from start (depth)
   - h(n): estimated cost to goal (heuristic)
   - Guides search toward most promising states

5. ✅ INTELLIGENT SELECTION
   - Priority queue maintains states by f(n)
   - Always expands lowest-cost state first
   - Visited set prevents infinite loops

6. ✅ OPTIMAL DECISION-MAKING
   - A* guarantees shortest path
   - Fewer nodes explored than uninformed search
   - Heuristic quality affects exploration efficiency

Real-world Applications:
• Robot path planning
• Game state solver
• Logistics optimization
• Route planning with distance estimates
• AI game AI (puzzles, chess)
    """)
