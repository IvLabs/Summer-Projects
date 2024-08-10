from pyamaze import maze,agent,COLOR

#Maze and agent
m=maze(9,9)
m.CreateMaze(5,5,loopPercent=10)
a=agent(m,shape='arrow',footprints=True)
b=agent(m,shape='arrow',footprints=True,color=COLOR.red)



#function for bfs
def bfs(grid):
    ed=(5,5)
    st=(9,9)

    queue=[st]
    visited=[st]
    bfspath={}

    while queue:
        (x,y)=queue.pop(0)
        if (x,y)==ed:
            break
        
        #for movement
        mover={'E':0,'W':0,'N':-1,'S':1}
        movec={'E':1,'W':-1,'N':0,'S':0}
        for d in 'EWNS':
            if m.maze_map[(x,y)][d]==True:
                nx=x+mover[d]
                ny=y+movec[d]

                if (nx,ny) not in visited:
                    queue.append((nx,ny))
                    visited.append((nx,ny))
                    bfspath[(nx,ny)]=(x,y)
    
    #To convert reverse path to forward
    pathb={}
    cell=ed
    while cell!=st:
        pathb[bfspath[cell]]=cell
        cell=bfspath[cell]

    return pathb
#Run the program
m.tracePath({a:bfs(m)})
m.tracePath({b:dfs(m)})
m.run()
