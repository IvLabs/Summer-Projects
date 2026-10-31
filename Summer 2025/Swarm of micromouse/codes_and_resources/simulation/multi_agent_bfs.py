from pyamaze import maze, agent ,COLOR, textLabel

def bfs(m,start):
    
    frontier = [start]
    explored = [start]
    bfsPath={}
    while len(frontier)>0:
        curr_cell= frontier.pop(0)
        if curr_cell==(16,16):
            break
        for d in 'NSEW':
            if m.maze_map[curr_cell][d]==True:
                if d=='N':
                    child_cell=(curr_cell[0]-1,curr_cell[1])
                elif d=='S':
                    child_cell=(curr_cell[0]+1,curr_cell[1])
                elif d=='E':
                    child_cell=(curr_cell[0],curr_cell[1]+1)
                elif d=='W':
                    child_cell=(curr_cell[0],curr_cell[1]-1)
                if child_cell in explored:
                    continue
                frontier.append(child_cell)
                explored.append(child_cell)
                bfsPath[child_cell]=curr_cell
    fwdPath={}
    cell=(16,16)
    while cell!=start:
        fwdPath[bfsPath[cell]]=cell
        cell=bfsPath[cell]
    return fwdPath


m = maze(31,31)
m.CreateMaze(x=16,y=16,loopPercent=40)

agent_blue = agent(m,31,31 ,footprints=True, filled=True)
path_blue = bfs(m, agent_blue.position)

agent_red = agent(m,31,1 ,footprints=True, filled=True, color=COLOR.red)
path_red = bfs(m, agent_red.position)

agent_yellow = agent(m,1,31 ,footprints=True, filled=True,color=COLOR.yellow)
path_yellow = bfs(m, agent_yellow.position)

m.markCells=[(16,16)]

m.tracePath({agent_blue:path_blue,agent_red:path_red,agent_yellow:path_yellow},delay=50,showMarked=True)

textLabel(m,'Algorithm - ','BFS')
textLabel(m,'Agent Blue Path Length - ',len(path_blue)+1)
textLabel(m,'Agent Red Path Length - ',len(path_red)+1)
textLabel(m,'Agent Yellow Path Length - ',len(path_yellow)+1)
m.run()