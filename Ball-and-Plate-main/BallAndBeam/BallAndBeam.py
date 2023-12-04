import matplotlib.pyplot as plt

kp=10
kd=10
ki=0

m=0.11
R=0.015
d=0.03
g=9.8
L=1
j=9.99*(10**(-6))
r=0.20
alpha=0
theta=0
t=0
dt=0.01
vn=0
xn=0
eo=r-xn
ei=0
c=0

position=[]
time=[]
error=[]
reference=[]

while(t<10):
    if abs((r*9/10)-xn)<=0.01 and t<3 and c==0:
        print("time = ",t)
        c=1
    
    e=r-xn
    ed=(e-eo)/dt
    ei=ei+(e*dt)
    eo=e

    time.append(t)
    position.append(xn*100)
    reference.append(r*100)
    error.append(e*100)
    
    theta=(e*kp)+(ed*kd)+(ei*ki)
    alpha=d*theta/L
    a=m*g*alpha*(R**2)/(j+(m*(R**2)))
    vn=vn+a*dt
    xn=xn+vn*dt
    vo=vn
    xo=xn
    t=t+dt
    
print("max error % is ",(-min(error))/r)
plt.plot(time,reference,linestyle='dashed')
plt.plot(time,position)
plt.plot(time,error)
plt.xlabel("T")
plt.ylabel("x and e")
r_title= 'desired position = '+str(r*100) +' cm'
plt.title(r_title)
plt.show()
