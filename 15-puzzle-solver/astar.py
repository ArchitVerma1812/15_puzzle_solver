"""
The A* algorithm implementation for solving the 15-puzzle problem.

The `a_star_15_puzzle` function takes the start and goal puzzle configurations as input
and returns the sequence of puzzle states that solves the puzzle using the A* algorithm.

The `manhattan_distance` function calculates the Manhattan distance heuristic for the 15-puzzle
which is used to estimate the cost to reach the goal state from the current state.

The `find_blank` function finds the position of zero state.

The `get_neighbors` function generates the possible moves.

The `swap` function swaps the positions of two tiles in the puzzle.

Bibliography:
https://www.geeksforgeeks.org/a-search-algorithm/

Authors:
Archit Verma

A-star algorithm 15-puzzle solver

Requirements: heapq
"""

import heapq

def manhattan_distance(puzzle, goal):
    """Heuristic function for calculating Manhattan distance."""
    distance = 0
    for row in range(4):
        for col in range(4):
            value = puzzle[row][col]
            # Skip the distance calculation for the 0-tile (blank space)
            if value != 0:
                target_row, target_col = divmod(value - 1, 4)
                distance += abs(row - target_row) + abs(col - target_col)
    return distance

def find_blank(puzzle):
    """Finds the position of the 0-tile (blank space) in the puzzle."""
    for row in range(4):
        for col in range(4):
            if puzzle[row][col] == 0:
                return row, col
    return None

def get_neighbors(position):
    """Generates valid neighboring positions for the blank tile."""
    row, col = position
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col))  # Move up
    if row < 3:
        neighbors.append((row + 1, col))  # Move down
    if col > 0:
        neighbors.append((row, col - 1))  # Move left
    if col < 3:
        neighbors.append((row, col + 1))  # Move right
    return neighbors

def swap(puzzle, pos1, pos2):
    """Creates a new puzzle state by swapping two tile positions."""
    new_puzzle = [row[:] for row in puzzle]  # Deep copy of the puzzle
    new_puzzle[pos1[0]][pos1[1]], new_puzzle[pos2[0]][pos2[1]] = (
        new_puzzle[pos2[0]][pos2[1]],
        new_puzzle[pos1[0]][pos1[1]],
    )
    return new_puzzle

def a_star_15_puzzle(start_puzzle, goal_puzzle):
    """A* algorithm implementation for solving the 15-puzzle problem."""
    open_list = []
    heapq.heappush(open_list, (0, start_puzzle))

    g_score = {str(start_puzzle): 0}
    parent_track = {}

    while open_list:
        _, current_puzzle = heapq.heappop(open_list)

        # Check if the current puzzle state matches the goal
        if current_puzzle == goal_puzzle:
            path = []
            while str(current_puzzle) in parent_track:
                path.append(current_puzzle)
                current_puzzle = parent_track[str(current_puzzle)]
            path.append(start_puzzle)
            return path[::-1]  # Reverse path to start from the initial state

        blank_pos = find_blank(current_puzzle)
        for neighbor_pos in get_neighbors(blank_pos):
            new_puzzle = swap(current_puzzle, blank_pos, neighbor_pos)
            new_g_score = g_score[str(current_puzzle)] + 1

            # Update g_score if new puzzle state is found or has a lower g_score
            if str(new_puzzle) not in g_score or new_g_score < g_score[str(new_puzzle)]:
                g_score[str(new_puzzle)] = new_g_score
                f_score = new_g_score + manhattan_distance(new_puzzle, goal_puzzle)
                heapq.heappush(open_list, (f_score, new_puzzle))
                parent_track[str(new_puzzle)] = current_puzzle

    return None  # Return None if no solution is found

def get_puzzle_input():
    """Reads user input for the 15-puzzle, row by row."""
    print("Enter the 15-puzzle row by row, using spaces between numbers:")
    puzzle = []
    for i in range(4):
        row = list(map(int, input(f"Row {i + 1}: ").split()))
        puzzle.append(row)
    return puzzle

# Example usage
if __name__ == "__main__":
    start_puzzle = get_puzzle_input()

    # Define goal state for 15-puzzle
    goal_puzzle = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 0]
    ]

    print("Solving...")
    path = a_star_15_puzzle(start_puzzle, goal_puzzle)

    if path:
        print("Solution found. Moves required:", len(path) - 1)
        for step in path:
            for row in step:
                print(row)
            print()
    else:
        print("No solution found.")
