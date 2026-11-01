from pyamaze import maze, agent, COLOR, textLabel

def bfs(m):
    start = (m.rows,m.cols)
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
    return fwdPath, explored


m=maze(31,31)
m.CreateMaze(16,16,loopPercent=40)
path, explore =bfs(m)

a=agent(m,footprints=True,filled=True)
m.tracePath({a:explore}, delay=10)
b= agent(m,footprints=True,filled=True,color=COLOR.green)
m.tracePath({b:path},delay=100)
l = textLabel(m,'Length of the path is ',len(path)+1)
m.run()