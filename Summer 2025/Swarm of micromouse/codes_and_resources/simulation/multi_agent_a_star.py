from pyamaze import maze, agent ,COLOR, textLabel
from queue import PriorityQueue

def h(cell1,cell2) :
    x1,y1=cell1
    x2,y2=cell2
    return abs(x1-x2)+abs(y1-y2)

def aStar(m,start):
    
    g_score = {cell:float('inf') for cell in m.grid}
    g_score[start]=0
    f_score = {cell:float('inf') for cell in m.grid}
    f_score[start] = h(start,(16,16))
    open = PriorityQueue()
    open.put((h(start,(16,16))+0,h(start,(16,16)),start))
    aPath = {}

    while not open.empty():
        currCell = open.get()[2]
        if currCell == (16,16):
            break
        for d in 'NSEW':
            if m.maze_map[currCell][d]==True:
                if d=='N':
                    childCell=(currCell[0]-1,currCell[1])
                elif d=='S':
                    childCell=(currCell[0]+1,currCell[1])
                elif d=='E':
                    childCell=(currCell[0],currCell[1]+1)
                elif d=='W':
                    childCell=(currCell[0],currCell[1]-1)

                temp_g_score = g_score[currCell]+1
                temp_f_score = temp_g_score + h(currCell,(16,16))

                if temp_f_score < f_score[childCell]:
                    g_score[childCell]= temp_g_score
                    f_score[childCell]= temp_f_score
                    open.put((temp_f_score,h(start,(16,16)),childCell))
                    aPath[childCell] = currCell
    fwdPath = {}
    cell = (16,16)
    while cell!=start:
        fwdPath[aPath[cell]]=cell
        cell=aPath[cell]
    return fwdPath


m = maze(31,31)
m.CreateMaze(x=16,y=16,loopPercent=40)

agent_blue = agent(m,31,31 ,footprints=True, filled=True)
path_blue = aStar(m, agent_blue.position)

agent_red = agent(m,31,1 ,footprints=True, filled=True, color=COLOR.red)
path_red = aStar(m, agent_red.position)

agent_yellow = agent(m,1,31 ,footprints=True, filled=True,color=COLOR.yellow)
path_yellow = aStar(m, agent_yellow.position)

m.markCells=[(16,16)]

m.tracePath({agent_blue:path_blue,agent_red:path_red,agent_yellow:path_yellow},delay=50,showMarked=True)

textLabel(m,'Algorithm - ','A*')
textLabel(m,'Agent Blue Path Length - ',len(path_blue)+1)
textLabel(m,'Agent Red Path Length - ',len(path_red)+1)
textLabel(m,'Agent Yellow Path Length - ',len(path_yellow)+1)
m.run()