# importing sympy package for making symbols, substitutions, matrix operations and its other features 
from sympy import *
from sympy import cos, sin

# making some symbols 
a,alpha,d,theta = symbols('a alpha d theta') # used in homogeneous transformation matrix
# symbols to be used in final fk equations
x_n,y_n,z_n,theta1,theta2,theta3= symbols('x_n,y_n,z_n,theta1,theta2,theta3')
l1,l2,l3= symbols('l1,l2,l3')

# Homogeneous Transformation Matrix based on DH parameters (a,alpha,d,theta) 
T=Matrix([[cos(theta), -sin(theta)*cos(alpha), sin(theta)*sin(alpha), a*cos(theta)], 
            [sin(theta), cos(alpha)*cos(theta), -sin(alpha)*cos(theta), a*sin(theta)], 
            [0, sin(alpha), cos(alpha), d], 
            [0, 0, 0, 1]])

def CalcTransformation():
    TransMatrix=eye(4)  # creating an identity matrix of size 4
    for i in range(n):
        # matrix for transformation of frame i+1 with respect to frame i
        Mat=T.subs([(a,inp_a[i]), (alpha, inp_alpha[i]), (d, inp_d[i]), (theta, inp_theta[i])])
        HomoMat.append(Mat)  # HomoMat to store all the transformation matrices for each transformations
        TransMatrix = TransMatrix*Mat  # calculating the transformation of (i+1)th frame with reaspect to frame 0
    return TransMatrix
    
# function to generate equations with parameters representing coods in frame n which are mapped to frame 0
def GenerateEquations(pos_x,pos_y,pos_z):
    x1,x=0,[]
    e=Matrix(4,1,[pos_x,pos_y,pos_z,1]) # making a matrix of 4*1 having symbols and values
    f=TransformationMat[:] # converting sympy matrix into a list
    for i in range(12): # since first three rows are of importance in 4*4 matrix
        x1=x1+f[i]*e[int(i%4)]
        if(i%4==3):
            x.append(x1) # extracting the equations and appending into x[]
            x1=0
    return x

if __name__ == "__main__":
    
    # values are taken accordingly for our planar robotic arm in terms of symbols (can be modified for some other robots)
    n=3  # no. of links
    inp_theta=[theta1,theta2,theta3] # joint angles
    inp_a=[l1,l2,l3] # link lengths
    inp_alpha=[0,0,0] # link twists
    inp_d=[0,0,0] # link offsets
    HomoMat=[] # for storing transformation matrices

    print("\n\n Generalised Transformation matrix is \n")
    pretty_print(T)

    TransformationMat=CalcTransformation() # calculating the transformation matrix
    TransformationMat=trigsimp(TransformationMat) # simplifying the trignometric expressions using sympy
    print("\n\n\n Transformation matrix for frame 3 with respect to frame 0 is \n")
    pretty_print(TransformationMat)

    j=GenerateEquations(x_n,y_n,z_n)
    print("\n\n Generalised Equations are: ")
    print("x_equation = ",j[0],"\ny_equation = ",j[1],"\nz_equation = ",j[2],"\n")

    eqn=Matrix(3,1,j)
    print("\n Symbolic representation of transformation equations are:\n")
    pretty_print(eqn)
    print("\n")