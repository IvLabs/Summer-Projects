from pyamaze import agent, maze, COLOR

# n = int(input("> "))
n = 16

maze1 = maze(n, n)
maze1.CreateMaze(n//2, n//2, loopPercent=20)

goal = (n//2, n//2)
start = (n, n)

pos_change = {'N':(-1, 0), 'E':(0, 1), 'S':(1, 0), 'W':(0, -1)}


def Flood(maze_map: dict, goal: tuple):
    val_map = {}
    val_map[goal] = 0
    queue = [goal]
    visited = []

    while queue:
        curpos = queue[0]
        queue = queue[1:]
        visited.append(curpos)

        for i in "NESW":
            if maze_map[curpos][i] == 1:
                pos = (curpos[0] + pos_change[i][0], curpos[1] + pos_change[i][1])
                if pos not in val_map:
                    val_map[pos] = val_map[curpos] + 1
                elif val_map[pos] > val_map[curpos] + 1:
                    val_map[pos] = val_map[curpos] + 1
                if pos not in queue and pos not in visited:
                    queue.append(pos)

    return val_map


def NextPosFinder(maze_map, start, goal):
    path = {}
    curpos = start
    val_map = Flood(maze_map, goal)

    neighbors = [(curpos[0] + pos_change[i][0], curpos[1] + pos_change[i][1]) for i in "NEWS" if maze_map[curpos][i]]
    minval = val_map[curpos]

    for pos in neighbors:
        if val_map[pos] < minval:
            minval = val_map[pos]
            nextpos = pos

    return nextpos


def FloodFill(start, goal):

    maze_map = {}

    for i in range(1, 17):
        for j in range(1, 17):
            maze_map[(i, j)] = {'N':1, 'E':1, 'S':1, 'W':1}
            if i == 1:
                maze_map[(1, j)]['N'] = 0
            if i == 16:
                maze_map[(16, j)]['S'] = 0
            if j == 1:
                maze_map[(i, 1)]['W'] = 0
            if j == 16:
                maze_map[(i, 16)]['E'] = 0

    path = {}
    forwpath = []
    revpath = []
    curpos = start

    while curpos != goal:
        maze_map = UpdateMap(maze_map, curpos)
        nextpos = NextPosFinder(maze_map, curpos, goal)
        forwpath.append(nextpos)
        curpos = nextpos

    while curpos != start:
        maze_map = UpdateMap(maze_map, curpos)
        nextpos = NextPosFinder(maze_map, curpos, start)
        revpath.append(nextpos)
        curpos = nextpos

    while curpos != goal:
        maze_map = UpdateMap(maze_map, curpos)
        nextpos = NextPosFinder(maze_map, curpos, goal)
        path[curpos] = nextpos
        curpos = nextpos

    return path, forwpath, revpath


def UpdateMap(maze_map, curpos):
    invdir = {'N':'S', 'E':'W', 'S':'N', 'W':'E'}

    maze_map[curpos] = maze1.maze_map[curpos]

    for i in "NESW":
        pos = (curpos[0] + pos_change[i][0], curpos[1] + pos_change[i][1])
        if maze1.maze_map[curpos][i] == 0 and pos in maze1.maze_map:
            maze_map[pos][invdir[i]] = 0

    return maze_map


path, forwpath, revpath = FloodFill(start, goal)

ag1 = agent(maze1, shape = 'arrow', footprints=True)
ag2 = agent(maze1, x=8, y=8, shape = 'arrow', footprints=True, goal=(16, 16), color=COLOR.green)
ag3 = agent(maze1, shape = 'arrow', footprints=True, color=COLOR.red)
ag4 = agent(maze1, filled=True, footprints=True)

maze1.tracePath({ag1:forwpath}, delay = 150)
maze1.tracePath({ag2:revpath}, delay = 150)
maze1.tracePath({ag4:path}, delay = 150)
maze1.tracePath({ag3:maze1.path}, delay = 150)

maze1.run()
