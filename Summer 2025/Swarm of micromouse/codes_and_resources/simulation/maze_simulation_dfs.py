from pyamaze import maze, agent ,COLOR, textLabel


def dfs(m):
    start = (m.rows,m.cols)
    frontier = [start]
    explored = [start]
    dfsPath = {}
    while len(frontier)>0 :
        currCell = frontier.pop()
        if currCell==(1,1) :
            break
        for d in 'ESNW' :
            if m.maze_map[currCell][d] == True :
                if d=='N':
                    childCell=(currCell[0]-1,currCell[1])
                elif d=='S':
                    childCell=(currCell[0]+1,currCell[1])
                elif d=='E':
                    childCell=(currCell[0],currCell[1]+1)
                elif d=='W':
                    childCell=(currCell[0],currCell[1]-1)
                if childCell in explored :
                    continue

                frontier.append(childCell)
                explored.append(childCell)
                dfsPath[childCell] = currCell
    fwdPath = {}
    cell = (1,1)
    while cell != start :
        fwdPath[dfsPath[cell]]=cell
        cell = dfsPath[cell]
    return fwdPath

m = maze(10,10)
m.CreateMaze(loopPercent=50)
path = dfs(m)

a = agent(m , footprints=True, filled=True)
m.tracePath({a:path})
l = textLabel(m,'Length of the shortest path is ',len(path)+1)
m.run()