import sympy as sp   # importing sympy package for making symbols, substitutions, matrix operations and its other features 
from sympy import cos, sin # importing cos,sin seperately for their easy access
import matplotlib.pyplot as plt # importing pyplot from matplotlib for a 3D plot


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
    global theta1_guess,theta2_guess,theta3_guess,theta_guess # using global variables
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
        theta1_set.append(theta1_guess)
        theta2_set.append(theta2_guess)
        theta3_set.append(theta3_guess)
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

def in_range(p):
    if(p%(2*sp.pi)<=sp.pi):
        p=p%(2*sp.pi)
    else:
        p=p%(2*sp.pi)-(2*sp.pi)
    return p
    
def plot_3D():  # plotting the values of angles calculated in each iteration
    fig=plt.figure()
    ax=plt.axes(projection='3d')
    ax.plot3D(theta1_set,theta2_set,theta3_set)
    ax.scatter3D(theta1_set,theta2_set,theta3_set,marker='o')
    ax.set_xlabel("theta 1 values")
    ax.set_ylabel("theta 2 values")
    ax.set_zlabel("theta 3 values")
    plt.title("Changes in values of theta1,theta2,theta3 after each iteration")
    plt.show()

if __name__=="__main__":
    theta1,theta2,theta3 = sp.symbols('theta1,theta2,theta3')
    l1,l2,l3=9.7,8.4,7.7
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
    theta1_set,theta2_set,theta3_set=[theta1_guess],[theta2_guess],[theta3_guess]
    theta_guess=sp.Matrix(3,1,[theta1_guess,theta2_guess,theta3_guess])

    jacobian_inv=jacobian.inv() 
    theta1_guess,theta2_guess,theta3_guess=calc()
    print("\n\n Angles being plotted are: ",float(theta1_guess),',',float(theta2_guess),',',float(theta3_guess))
    plot_3D()

