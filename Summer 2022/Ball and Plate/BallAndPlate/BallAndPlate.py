import matplotlib.pyplot as plt

kpx=0.05
kix=0
kdx=0.1

kpy=0.01
kiy=0
kdy=0.1

mb=0.11
rb=0.02
rx=1/2
ry=1/2
vmax=4/100
mp=0.1
ip=0.5
ib=1.76*10**-6
g=9.81
dt=0.01
ax=0
ay=0
vx=0
vy=0
x=0.8
y=0.1
t=0
c=0
d=0

ex=0
exo=0
eix=0
edx=0

ey=0
eyo=0
eiy=0
edy=0

xlist=[]
ylist=[]
tlist=[]
exlist=[]
eylist=[]
rlist=[]

while(t<50):
    if abs((rx*9/10)-x)<=0.01 and t<3 and c==0:
        print("time_x = ",t)
        c=1
    if abs((ry*9/10)-y)<=0.01 and t<3 and d==0:
        print("time_y = ",t)
        d=1
    
    ex=rx-x
    ey=ry-y

    edx=(ex-exo)/dt
    edy=(ey-eyo)/dt

    eix=eix+ex*dt
    eiy=eiy+ey*dt

    ux=ex*kpx+edx*kdx+eix*kix
    uy=ey*kpy+edy*kdy+eiy*kiy

    ax=7*g*ux/5
    vx=vx+ax*dt
    x=x+vx*dt
    ay=7*g*uy/5
    vy=vy+ay*dt
    y=y+vy*dt
    
    xlist.append(x)
    ylist.append(y)
    exlist.append(ex)
    eylist.append(ey)
    tlist.append(t)
    rlist.append(rx)
    
    t=t+dt
    exo=ex
    eyo=ey
   
plt.plot(tlist,rlist,linestyle='dashed')
plt.plot(tlist,ylist)
plt.plot(tlist,eylist)
plt.xlabel("T")
plt.ylabel("x and e(x)")
r_title= 'x_desired = '+str(rx)+' m' 
plt.title(r_title)

plt.figure()

plt.plot(tlist,rlist,linestyle='dashed')
plt.plot(tlist,xlist)
plt.plot(tlist,exlist)
plt.xlabel("T")
plt.ylabel("y and e(y)")
r_title= 'y_desired = '+str(ry)+' m' 
plt.title(r_title)

plt.figure()

plt.plot(xlist,ylist)
plt.xlim(0,1)
plt.ylim(0,1)
plt.xlabel("x")
plt.ylabel("y")
plt.title('Trajectory of ball')
plt.show()

