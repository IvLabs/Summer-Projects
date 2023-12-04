import sympy as sp   # importing sympy package for making symbols, substitutions, matrix operations and its other features 
from sympy import cos, sin # importing cos,sin seperately for their easy access
import numpy as np
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator) # for modifying major and minor divisions along axes
import matplotlib.pyplot as plt # importing pyplot from matplotlib for plots
import matplotlib.animation as animation

# making some symbols used in the fk equations
theta1,theta2,theta3 = sp.symbols('theta1,theta2,theta3')

def calc_Jacobian():
    j=[]  # calculating jacobian
    j.append(sp.diff(x1,theta1))
    j.append(sp.diff(x1,theta2))
    j.append(sp.diff(x1,theta3))
    j.append(sp.diff(y1,theta1))
    j.append(sp.diff(y1,theta2))
    j.append(sp.diff(y1,theta3))
    j.append(sp.diff(z_angle,theta1))
    j.append(sp.diff(z_angle,theta2))
    j.append(sp.diff(z_angle,theta3))
    jac=sp.Matrix(3,3,j)
    print("\n\n----------------------------------JACOBIAN-----------------------------------\n")
    sp.pretty_print(jac)
    return jac

def lines_point(p,val_i,val_f):
    if(val_i[0]<=val_f[0]):
        x_mat=np.linspace(val_i[0],val_f[0],p)
    else:
        x_mat=np.linspace(val_f[0],val_i[0],p)
        x_mat=np.flip(x_mat)
    if(val_i[1]<=val_f[1]):
        y_mat=np.linspace(val_i[1],val_f[1],p)
    else:
        y_mat=np.linspace(val_f[1],val_i[1],p)
        y_mat=np.flip(y_mat)
    if(val_i[2]<=val_f[2]):
        z_mat=np.linspace(val_i[2],val_f[2],p)
    else:
        z_mat=np.linspace(val_f[2],val_i[2],p)
        z_mat=np.flip(z_mat)
    for i in range(0,p):
        point_x.append(x_mat[i])
        point_y.append(y_mat[i])
        point_z.append(z_mat[i])

def i_pt():
    lines_point(15,[3.25,22,1.7873],[4.75,22,1.89687])
    lines_point(10,[4.75,22,1.89687],[4,22,1.823])
    lines_point(20,[4,22,1.823],[4,20,2.1076])
    lines_point(10,[4,20,2.1076],[3.25,20,2.0177])
    lines_point(20,[3.25,20,2.0177],[4.75,20,2.1576])

def v_pt():
    lines_point(15,[4.75,20.5,2.1152],[5.5,19,2.2052])
    lines_point(15,[5.5,19,2.2052],[6.5,20.5,2.1152])

def l_pt():
    lines_point(20,[6.25,20,2.1245],[6.25,18,2.1845])
    lines_point(15,[6.25,18,2.1845],[7.5,18,2.1245])

def a_pt():
    lines_point(20,[8,18,2.205],[9,20,1.8545])
    lines_point(20,[9,20,1.8545],[9.7,18,2.0517])
    lines_point(10,[9.7,18,2.0517],[9.4375,18.75,2.015173])
    lines_point(10,[9.4375,18.75,2.015173],[8.375,18.75,2.0517])

def b_pt():
    lines_point(20,[10,18,1.4451],[10,20,1.4451])
    centre_x,centre_y,a,b=10,19.5,1,0.5
    arr=np.linspace(-np.pi/2,np.pi/2,25)
    arr=np.flip(arr)
    for i in range(0,25):
        point_x.append(centre_x+a*cos(arr[i]))
        point_y.append(centre_y+b*sin(arr[i]))
        point_z.append(1.445173)
    centre_x,centre_y,a,b=10,18.5,1,0.5
    for i in range(0,25):
        point_x.append(centre_x+a*cos(arr[i]))
        point_y.append(centre_y+b*sin(arr[i]))
        point_z.append(1.445173)

def s_pt():
    lines_point(20,[12.5,22,1.245173],[11,22,1.245173])
    lines_point(10,[11,22,1.245173],[11,21,1.245173])
    lines_point(20,[11,21,1.245173],[12.5,21,1.245173])
    lines_point(10,[12.5,21,1.245173],[12.5,20,1.245173])
    lines_point(20,[12.5,20,1.245173],[11,20,1.245173])

def calc_angles(x_p,y_p,z_p):

    x1=l1*cos(theta1)+l2*cos(theta1+theta2)+l3*cos(theta1+theta2+theta3)-x_p
    y1=l1*sin(theta1)+l2*sin(theta1+theta2)+l3*sin(theta1+theta2+theta3)-y_p
    z_angle=theta1+theta2+theta3-z_p
    func_mat=sp.Matrix(3,1,[x1,y1,z_angle])

    i,count=True,0
    global theta1_guess,theta2_guess,theta3_guess,theta_guess
    while(i):
        count=count+1
        jacobian_inv_value=jacobian_inv.subs([(theta1,theta1_guess),(theta2,theta2_guess),(theta3,theta3_guess)])
        func_mat_value=func_mat.subs([(theta1,theta1_guess),(theta2,theta2_guess),(theta3,theta3_guess)])
        theta_val=theta_guess-jacobian_inv_value*func_mat_value
        if(abs(theta_val[0]-theta_guess[0])<0.0000001 and abs(theta_val[1]-theta_guess[1])<0.0000001 and abs(theta_val[2]-theta_guess[2])<0.0000001 ):
            i=False # values approximated upto desired accuracy
        if(count==150):
            i=False
            print("terminated without approximating values")
        theta_guess=theta_val
        theta1_guess,theta2_guess,theta3_guess=theta_val[0],theta_val[1],theta_val[2]
        # changing initial values if not approximated within 40 iterations
        if(count==40):
            print([count])
            theta1_guess,theta2_guess,theta3_guess=1.0471975512,1.0471975512,1.0471975512 # pi/3
        if(count==80):
            print([count])
            theta1_guess,theta2_guess,theta3_guess=0.7853981634,0.7853981634,0.7853981634 # pi/4
        if(count==120):
            print([count])
            theta1_guess,theta2_guess,theta3_guess=1.5707963268,1.5707963268,1.5707963268 # pi/2
    theta1_guess,theta2_guess,theta3_guess=in_range(theta1_guess),in_range(theta2_guess),in_range(theta3_guess)
    theta1_set.append(float(theta1_guess))
    theta2_set.append(float(theta2_guess))
    theta3_set.append(float(theta3_guess))
    th1=round((theta1_guess*180/sp.pi),1)
    th2=round((theta2_guess*180/sp.pi+90),1)
    th3=round((90-theta3_guess*180/sp.pi),1)
    send_theta1.append(th1)
    send_theta2.append(th2)
    send_theta3.append(th3)

def in_range(p):
    if(p%(2*sp.pi)<=sp.pi):
        p=p%(2*sp.pi)
    else:
        p=p%(2*sp.pi)-(2*sp.pi)
    return p

def animate(i):
    x1,y1=0,0
    angle_1,angle_2,angle_3=theta1_set[i],theta2_set[i],theta3_set[i]
    if(angle_1<0 or abs(angle_2)>1.57 or abs(angle_3)>1.57):
        print([angle_1,angle_2,angle_3,i,"crossed"])
    elif(angle_1<0.1745 or abs(angle_2)>1.53 or abs(angle_3)>1.53):
        print([angle_1,angle_2,angle_3,i,"close"])
    x2=l1*cos(angle_1)
    y2=l1*sin(angle_1)
    x3=x2+l2*cos(angle_1+angle_2)
    y3=y2+l2*sin(angle_1+angle_2)
    x4=x3+l3*cos(angle_1+angle_2+angle_3)
    y4=y3+l3*sin(angle_1+angle_2+angle_3)
    
    link1.set_data([x1,x2],[y1,y2])
    link2.set_data([x2,x3],[y2,y3])
    link3.set_data([x3,x4],[y3,y4])
    trace_x.append(x4)
    trace_y.append(y4)
    plt.scatter(trace_x,trace_y,marker='.',lw=0.01,color='orange')
    return link1,link2,link3


if __name__=="__main__":

    theta1,theta2,theta3 = sp.symbols('theta1,theta2,theta3')
    l1,l2,l3=9.7,8.4,7.7  # links lengths for our planar robotic arm
    x1=l1*cos(theta1)+l2*cos(theta1+theta2)+l3*cos(theta1+theta2+theta3)
    y1=l1*sin(theta1)+l2*sin(theta1+theta2)+l3*sin(theta1+theta2+theta3)
    z_angle=theta1+theta2+theta3
    func_mat=sp.Matrix(3,1,[x1,y1,z_angle])
    print("\n\n----------------------------------EQUATIONS-----------------------------------\n\n")
    sp.pretty_print(func_mat)

    jacobian=calc_Jacobian()
    theta1_val,theta2_val,theta3_val=0,0,0
    theta_val=sp.Matrix(3,1,[theta1_val,theta2_val,theta3_val])
    theta1_guess,theta2_guess,theta3_guess=1.0472,1.0472,1.0472
    theta_guess=sp.Matrix(3,1,[theta1_guess,theta2_guess,theta3_guess])

    jacobian_inv=jacobian.inv() 
    theta1_set,theta2_set,theta3_set=[],[],[]
    point_x,point_y,point_z=[],[],[]
    send_theta1,send_theta2,send_theta3=[],[],[]

    i_pt(),v_pt(),l_pt(),a_pt(),b_pt(),s_pt()

    loop_c=len(point_x)
    print("\n",point_x,"\n\n",point_y,"\n\n",point_z,"\n\n",loop_c,"\n\n")

    for k in range(0,loop_c):
        calc_angles(point_x[k],point_y[k],point_z[k])

    print(send_theta1,"\n\n",send_theta2,"\n\n",send_theta3,"\n\n",len(send_theta3))


# plotting the axes and the lines and repeatedly setting data for the line plot in each frame
    sum_link_len=l1+l2+l3
    fig=plt.figure()
    trace_x,trace_y=[],[]
    axes=plt.axes(xlim =(-0.3*sum_link_len,1.02*sum_link_len), ylim =(-0.2*sum_link_len,1.02*sum_link_len))
    axes.xaxis.set_major_locator(MultipleLocator(2))
    axes.yaxis.set_major_locator(MultipleLocator(2))
    axes.xaxis.set_minor_locator(AutoMinorLocator(2))
    axes.yaxis.set_minor_locator(AutoMinorLocator(2))
    axes.grid(which='major', color='#CCCCCC', linestyle='--')
    axes.grid(which='minor', color='#CCCCCC', linestyle=':')
    link1,=axes.plot([],[],linewidth=2.5,color='blue',marker='o')
    link2,=axes.plot([],[],linewidth=2.5,color='green',marker='o')
    link3,=axes.plot([],[],linewidth=2.5,color='orange',marker='o')
    anim = animation.FuncAnimation(fig, animate,frames = loop_c, interval = 3, repeat=False)

    fig.suptitle('Tracing IvLabs with Robotic Arm', fontsize=14)
    # writergif = animation.PillowWriter(fps=10) 
    # anim.save('Tracing IvLabs.gif', writer=writergif)
    plt.show()

