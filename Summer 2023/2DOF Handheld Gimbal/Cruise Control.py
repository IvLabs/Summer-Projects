import numpy as np
import matplotlib.pyplot as plt

# Constants
m = 50  # Mass of car
b = 4  # Air damping constant
u = 100  # Reference speed

# Initial conditions
v = [0, 0]  # Speedometer reading/output
e = [u]  # Error term, initial error = reference speed - initial speed = u - 0
f = [0, 100]  # Engine force, initially the engine exerts some random force, say 100 units
y = v  # Output
count = 1  # Number of elements in the error list

# Function to calculate the error
def error(u, v):
    e.append(u - v[-1])

# PID Controller function
def PID(e):  # In time interval dt = 0.1s
    global count
    a = 4 #4
    c = 500 #2
    d = 0.01 #0.024
    # a = Kp = 4, c = Kd/0.1, d = Ki*(0.1/2) #Trapezoid method of integration
    f.append(a * e[-1] + c * abs(e[-1] - e[-2]) + d * ((2 * sum(e)) - e[0] - e[-1]))
    count += 1

# Function to calculate velocity
def vel(f, v):
    v.append((f[-1] + (m * v[-2] / 0.1)) / (b + (m / 0.1)))

# Initial velocity and error calculation
vel(f, v)
error(u, v)

# Initialize count and setpoint threshold
count = 0
max_count = 10000  # Maximum number of iterations to prevent infinite loops

# Main loop to control and stabilize speed
while count < max_count:
    # Perform PID control
    PID(e)
    
    # Update velocity and error
    vel(f, v)
    error(u, v)
    
    # Check if the error is within the acceptable range
    if abs(e[-1]) < 0.0001:
        # If error is small enough, consider the system stabilized
        break
    
    count += 1

# Plotting the results
font1 = {'family': 'serif', 'color': 'darkred', 'size': 20}
font2 = {'family': 'serif', 'color': 'black', 'size': 15}

# Plotting the error over time
x_coords = [0.1 * x for x in range(len(e))]
y_coords = np.array(e)
y_coords_2 = np.zeros(len(e))
plt.plot(x_coords, y_coords, x_coords, y_coords_2)
plt.xlabel("Time", fontdict=font2)
plt.ylabel("Error", fontdict=font2)
plt.title('Cruise Control System', fontdict=font1)
plt.show()

# Plotting the engine force over time
f.pop(0)
x_coords = [0.1 * x for x in range(len(f))]
y_coords = np.array(f)
plt.plot(x_coords, y_coords)
plt.xlabel("Time", fontdict=font2)
plt.ylabel("Force applied by engine", fontdict=font2)
plt.title('Cruise Control System', fontdict=font1)
plt.show()

# Plotting the velocity over time
x_coords = [0.1 * x for x in range(len(v))]
y_coords = np.array(v)
y_coords_2 = np.full(len(v), u)
plt.plot(x_coords, y_coords, x_coords, y_coords_2)
plt.xlabel("Time", fontdict=font2)
plt.ylabel("Velocity of car", fontdict=font2)
plt.title('Cruise Control System', fontdict=font1)
plt.show()
