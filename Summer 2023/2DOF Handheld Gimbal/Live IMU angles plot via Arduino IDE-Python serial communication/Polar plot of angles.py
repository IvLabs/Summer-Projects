import numpy as np
import matplotlib.pyplot as plt
import serial
import time

# Initialize serial connection to Arduino
#Shut the serial monitor in Arduino IDE to establish serial communication
#Update the serial port and baud rate to match the settings in the Arduino IDE.
arduinoData = serial.Serial('com5', 115200)
time.sleep(2)  # Allow time for the connection to establish

# Initialize variables
angles_x = [] #Rotation along x-axis as detected by IMU
angles_y = [] #Rotation along y-axis as detected by IMU
fig = plt.figure()
ax = plt.axes(projection='polar')
temp = 0

while True:
    # Wait for data from Arduino
    while arduinoData.inWaiting() == 0:
        pass

    # Read and process data
    dataPacket = arduinoData.readline()
    dataPacket = dataPacket.decode('utf-8').strip('\r\n')
    splitPacket = list(map(float, dataPacket.split(',')))

    angles_x.append(splitPacket[0])
    angles_y.append(splitPacket[1])
    print(splitPacket)

    # Polar plot of data
    a = [0, angles_x[-1]]
    b = [0, angles_y[-1]]
    c = [0, 1]
    ax.plot(a, c, b, c, linestyle='-')
    plt.pause(0.05)
    
    # Clear previous plot for the next iteration
    ax.clear()
    temp += 1

plt.show()
