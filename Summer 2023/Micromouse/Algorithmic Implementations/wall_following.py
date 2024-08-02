from pyamaze import maze, agent

# Function to rotate the direction path clockwise
def Clockwise():
    global pathFind
    k_lst = list(pathFind.keys())
    v_lst = list(pathFind.values())
    v_rot = [v_lst[-1]] + v_lst[:-1]
    # Updating the direction path for the updated dictionary
    pathFind = dict(zip(k_lst, v_rot))

# Function to rotate the direction path anti-clockwise
def AClockwise():
    global pathFind
    k_lst = list(pathFind.keys())
    v_lst = list(pathFind.values())
    v_rot = v_lst[1:] + [v_lst[0]]
    # Updating the direction path for the updated dictionary
    pathFind = dict(zip(k_lst, v_rot))

# Function to move forward based on the current direction
def moveF(cell):
    if pathFind['forward'] == 'E':
        return (cell[0], cell[1] + 1), 'E'
    elif pathFind['forward'] == 'W':
        return (cell[0], cell[1] - 1), 'W'
    elif pathFind['forward'] == 'N':
        return (cell[0] - 1, cell[1]), 'N'
    elif pathFind['forward'] == 'S':
        return (cell[0] + 1, cell[1]), 'S'

# Function to make the agent follow the left wall until it reaches the goal
def wallFollower(m, goal):
    global pathFind
    path = ''
    # Initializing the direction path
    pathFind = {'forward': 'N', 'left': 'W', 'back': 'S', 'right': 'E'}
    current = (m.rows, m.cols)
    path1 = ''
    while True:
        if current == goal:
            break
        if m.maze_map[current][pathFind['left']] == 0:
            if m.maze_map[current][pathFind['forward']] == 0:
                Clockwise()  # Make a clockwise turn
            else:
                current, d = moveF(current)  # Move forward
                path += d
                path1 += d
        else:
            AClockwise()  # Make an anti-clockwise turn
            current, d = moveF(current)  # Move forward
            path += d
            path1 += d
    return path, path1

# Create maze and agent
m = maze(11, 10)
m.CreateMaze(loopPercent=100)
agent1 = agent(m)

# Define the goal coordinates
goal = (6, 4)

# Get the paths for the agent to follow the left wall
path, path1 = wallFollower(m, goal)

# Trace and run the path for the agent
agent1_path = agent1.tracePath(path1)
m.run()
