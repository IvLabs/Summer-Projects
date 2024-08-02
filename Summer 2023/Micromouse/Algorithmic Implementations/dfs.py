from pyamaze import maze, agent

def dfs(m):
    # Initialize starting point and data structures
    start = (m.rows, m.cols)
    stack = [start]  # Stack for DFS traversal
    visited = [start]  # List to keep track of visited cells
    dfspath = {}  # Dictionary to store the DFS path

    # Perform DFS traversal
    while len(stack) > 0:
        current = stack.pop()  # Pop the top cell from the stack

        if current == (1, 1):
            break  # If we reach the destination, break the loop

        # Explore neighboring cells in the order East, South, West, North
        for direction in "ESWN":
            if m.maze_map[current][direction]:
                if direction == "E":
                    next_cell = (current[0], current[1] + 1)
                elif direction == "S":
                    next_cell = (current[0] + 1, current[1])
                elif direction == "W":
                    next_cell = (current[0], current[1] - 1)
                elif direction == "N":
                    next_cell = (current[0] - 1, current[1])

                if next_cell not in visited:
                    stack.append(next_cell)  # Push the neighboring cell onto the stack
                    visited.append(next_cell)  # Mark it as visited
                    dfspath[next_cell] = current  # Store the path

    # Reconstruct the original path from the destination to the starting point
    original_path = {}
    current_cell = (1, 1)
    while current_cell != start:
        original_path[dfspath[current_cell]] = current_cell
        current_cell = dfspath[current_cell]

    return original_path

# Create a maze and find the DFS path
maze_size = (10, 10)
m = maze(*maze_size)
m.CreateMaze()
dfs_path = dfs(m)

# Create an agent and trace the DFS path in the maze
a = agent(m)
m.tracePath({a: dfs_path})
m.run()
