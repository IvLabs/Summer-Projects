import matplotlib.pyplot as plt

kp=55
ki=50
kd=10

m=25
b=25 
vn=0
t=0
dt=0.1
r=60
eo=r-vn
ei=0
a=0

time=[]
velocity=[]
error=[]
rlist=[]

while t<20:
    if abs((r*9/10)-vn)<=0.5 and t<10:
        print("time = ",t)
        
    time.append(t)
    velocity.append(vn)
    rlist.append(r)
        
    e=r-vn
    error.append(e)
    ed=(e-eo)/dt
    ei=ei+(e*dt)
    eo=e
    
    u=(e*kp)+(ed*kd)+(ei*ki)
    a=(u-b*vn)/m
    vn=a*dt+vn
    t=t+dt
    
print("max error % is ",(-min(error))*100/r)
plt.plot(time,rlist)
plt.plot(time,velocity)
plt.plot(time,error)
plt.xlabel("T")
plt.ylabel("V and e")
r_title= 'Reference velocity = '+str(r)+'kmph' 
plt.title(r_title)
plt.show()
    
    
    
