from pyamaze import maze, agent ,COLOR, textLabel


def dfs(m,start):

    frontier = [start]
    explored = [start]
    dfsPath = {}
    while len(frontier)>0 :
        currCell = frontier.pop()
        if currCell==(16,16) :
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
    cell = (16,16)
    while cell != start :
        fwdPath[dfsPath[cell]]=cell
        cell = dfsPath[cell]
    return fwdPath

m = maze(31,31)
m.CreateMaze(x=16,y=16,loopPercent=40)

agent_blue = agent(m,31,31 ,footprints=True, filled=True)
path_blue = dfs(m, agent_blue.position)

agent_red = agent(m,31,1 ,footprints=True, filled=True, color=COLOR.red)
path_red = dfs(m, agent_red.position)

agent_yellow = agent(m,1,31 ,footprints=True, filled=True,color=COLOR.yellow)
path_yellow = dfs(m, agent_yellow.position)

m.markCells=[(16,16)]

m.tracePath({agent_blue:path_blue,agent_red:path_red,agent_yellow:path_yellow},delay=50,showMarked=True)

textLabel(m,'Algorithm - ','DFS')
textLabel(m,'Agent Blue Path Length - ',len(path_blue)+1)
textLabel(m,'Agent Red Path Length - ',len(path_red)+1)
textLabel(m,'Agent Yellow Path Length - ',len(path_yellow)+1)
m.run()