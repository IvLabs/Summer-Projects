import sympy as sp   # importing sympy package for making symbols, substitutions, matrix operations and its other features 
from sympy import cos, sin # importing cos,sin seperately for their easy access
import matplotlib.pyplot as plt # importing pyplot from matplotlib for a line plot
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator) # for modifying major and minor divisions along axes
from numpy import linspace
import matplotlib.animation as animation

# making some symbols used in the fk equations
theta1,theta2,theta3 = sp.symbols('theta1,theta2,theta3')

def get_coods():
# asking for desired position and orientation
    pt_x=float(input("\nEnter the desired x-coordinate of the end effector:   "))
    pt_y=float(input("Enter the desired y-coordinate of the end effector:   "))
    pt_z=float(input("Enter the desired orientation of the end effector in radians: "))
    return (pt_x,pt_y,pt_z)

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

def calc():
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
    return theta1_guess,theta2_guess,theta3_guess

def make_sets(r1,r2,r3):
    if(r1>=0):
        d1=linspace(0,r1,int(60*r1))
    else:
        d1=linspace(0,r1,int(60*r1))
        d1=d1*-1
    if(r2>=0):
        d2=linspace(0,r2,int(60*r2))
    else:
        d2=linspace(0,abs(r2),int(60*abs(r2)))
        d2=d2*-1
    if(r3>=0):
        d3=linspace(0,r3,int(60*r3))
    else:
        d3=linspace(0,abs(r3),int(60*abs(r3)))
        d3=d3*-1
    return d1,d2,d3

def in_range(p):
    if(p%(2*sp.pi)<=sp.pi):
        p=p%(2*sp.pi)
    else:
        p=p%(2*sp.pi)-(2*sp.pi)
    return p

def animate(i):

    if(i<l_set_1): # condition for link1 to move
        x1,y1=0,0
        x2,y2=l1*cos(th_set_1[i]),l1*sin(th_set_1[i])
        x3,y3=(l1+l2)*cos(th_set_1[i]),(l1+l2)*sin(th_set_1[i])
        x4,y4=(l1+l2+l3)*cos(th_set_1[i]),(l1+l2+l3)*sin(th_set_1[i])
        link1.set_data([x1,x2],[y1,y2])
        link2.set_data([x2,x3],[y2,y3])
        link3.set_data([x3,x4],[y3,y4])
        return link1,link2,link3
    elif(i<l_set_1+l_set_2 and i>=l_set_1): # condition for link2 to move
        x1,y1=0,0
        x2,y2=l1_xmax,l1_ymax
        x3,y3=l1_xmax+l2*cos(th_set_1[l_set_1-1]+th_set_2[i-l_set_1]),l1_ymax+l2*sin(th_set_1[l_set_1-1]+th_set_2[i-l_set_1])
        x4,y4=l1_xmax+(l2+l3)*cos(th_set_1[l_set_1-1]+th_set_2[i-l_set_1]),l1_ymax+(l2+l3)*sin(th_set_1[l_set_1-1]+th_set_2[i-l_set_1])
        link1.set_data([x1,x2],[y1,y2])
        link2.set_data([x2,x3],[y2,y3])
        link3.set_data([x3,x4],[y3,y4])
        return link1,link2,link3
    elif(i<l and i>=l_set_1+l_set_2): # condition for link3 to move
        x1,y1=0,0
        x2,y2=l1_xmax,l1_ymax
        x3,y3=l1_xmax+l2_xmax,l1_ymax+l2_ymax
        x4=l1_xmax+l2_xmax+l3*cos(th_set_1[l_set_1-1]+th_set_2[l_set_2-1]+th_set_3[i-l_set_1-l_set_2])
        y4=l1_ymax+l2_ymax+l3*sin(th_set_1[l_set_1-1]+th_set_2[l_set_2-1]+th_set_3[i-l_set_1-l_set_2])
        link1.set_data([x1,x2],[y1,y2])
        link2.set_data([x2,x3],[y2,y3])
        link3.set_data([x3,x4],[y3,y4])
        return link1,link2,link3


if __name__=="__main__":

    theta1,theta2,theta3 = sp.symbols('theta1,theta2,theta3')
    l1,l2,l3=9.7,8.4,7.7  # links lengths for our planar robotic arm
    pt_x,pt_y,pt_z=get_coods()
    # subtracting from the obtained fk equations for making the expressions equals to 0 (for Newton-Raphson implementation)
    x1=l1*cos(theta1)+l2*cos(theta1+theta2)+l3*cos(theta1+theta2+theta3)-pt_x
    y1=l1*sin(theta1)+l2*sin(theta1+theta2)+l3*sin(theta1+theta2+theta3)-pt_y
    z_angle=theta1+theta2+theta3-pt_z
    func_mat=sp.Matrix(3,1,[x1,y1,z_angle])
    print("\n\n----------------------------------EQUATIONS-----------------------------------\n\n")
    sp.pretty_print(func_mat)

    jacobian=calc_Jacobian()
    theta1_val,theta2_val,theta3_val=0,0,0
    theta_val=sp.Matrix(3,1,[theta1_val,theta2_val,theta3_val])
    theta1_guess,theta2_guess,theta3_guess=1.0472,1.0472,1.0472
    theta_guess=sp.Matrix(3,1,[theta1_guess,theta2_guess,theta3_guess])

    jacobian_inv=jacobian.inv() 
    theta1_guess,theta2_guess,theta3_guess = calc()
    print("\n\n Calculated angles are: ",theta1_guess,',',theta2_guess,',',theta3_guess)

# making sets of angles from 0 to animate to the final orientation
    th_set_1,th_set_2,th_set_3 = make_sets(float(theta1_guess),float(theta2_guess),float(theta3_guess))
    l_set_1,l_set_2,l_set_3 = len(th_set_1),len(th_set_2),len(th_set_3)
    l = l_set_1+l_set_2+l_set_3
    l1_xmax,l2_xmax = l1*cos(th_set_1[l_set_1-1]), l2*cos(th_set_1[l_set_1-1]+th_set_2[l_set_2-1])
    l1_ymax,l2_ymax = l1*sin(th_set_1[l_set_1-1]), l2*sin(th_set_1[l_set_1-1]+th_set_2[l_set_2-1])


# plotting the axes and the lines and repeatedly setting data for the line plot in each frame
    sum_link_len=l1+l2+l3
    fig=plt.figure()
    axes=plt.axes(xlim =(-0.2*sum_link_len,1.02*sum_link_len), ylim =(-0.3*sum_link_len,1.02*sum_link_len))
    axes.xaxis.set_major_locator(MultipleLocator(2))
    axes.yaxis.set_major_locator(MultipleLocator(2))
    axes.xaxis.set_minor_locator(AutoMinorLocator(2))
    axes.yaxis.set_minor_locator(AutoMinorLocator(2))
    axes.grid(which='major', color='#CCCCCC', linestyle='--')
    axes.grid(which='minor', color='#CCCCCC', linestyle=':')
    fig.suptitle('Inverse Kinematics to ('+str(pt_x)+','+str(pt_y)+')', fontsize=14)
    link1,=axes.plot([],[],linewidth=2.5,color='blue',marker='o')
    link2,=axes.plot([],[],linewidth=2.5,color='green',marker='o')
    link3,=axes.plot([],[],linewidth=2.5,color='orange',marker='o')
    anim = animation.FuncAnimation(fig, animate,frames = l, interval = 30, repeat=False)

    # writergif = animation.PillowWriter(fps=30) 
    # anim.save('IK_animation_from_0.gif', writer=writergif)
    plt.show()

