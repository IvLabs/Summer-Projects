# Micromouse
This is the official repository for the Micromouse project at IvLabs, VNIT Nagpur

## Objectives
The objectives of the summer internship were to create a compact( 8 x 8 cm) robot that can autonomously solve and obtain the fastest path for any given maze. 

## Methodology

### Software Implementation
In the initial weeks, we worked on implementing the maze solving algorithms in python. We implemented and explored a set of algorithms, namely

1.Wall Following:
    The bot just follows the walls till it reaches the  
    goal. Not very efficient as it is a brute force approach  and can run into loops 
    when there are dead ends and for this algorithm to work, the goal has to be in one of the corners .

![unnamed](https://github.com/ChinmayK0607/Micromouse/assets/114411195/c75196c7-b359-4f6c-813e-1bdc06cc3916) =100x200



2.BFS:
    Breadth First Search systematically examines all available nodes at a given level before delving deeper into the tree or graph structure or in this case, the maze.

![unnamed (2)](https://github.com/ChinmayK0607/Micromouse/assets/114411195/5c1c0090-bf98-4234-b390-1e8a5d37e98b)


3.DFS:
Depth First Search, on the other hand, delves as deeply as possible into a branch of nodes before backtracking to explore other branches.

![unnamed (1)](https://github.com/ChinmayK0607/Micromouse/assets/114411195/9875c933-78fc-4c69-aba6-03c77bc93ab8)


4.Flood Fill

![unnamed (3)](https://github.com/ChinmayK0607/Micromouse/assets/114411195/fdd92060-7501-4717-bc51-6b367a332059)



Code for each of the above mentioned algorithms can be found in ```Algorithmic Implementations``` Folder.

After this, we built a maze using corrugated sheets ,The dimensions used were 16 x 16 cell.The maze consists of  plus shaped holders that can be used to hold two or more sheets according to requirements.
Subsequently initiated work on hardware components, which involved tasks such as testing sensors and assembling the necessary equipment.

![image](https://github.com/ChinmayK0607/Micromouse/assets/114411195/ae7f2db2-d7bf-4d09-bff6-167788ed4e04)


The detailed hardware breakdown is mentioned below. 

We went with using sensor data for precise turning, and we were able to solve the maze.
Testing included 5 different mazes.

Image of the final bot:


![image](https://github.com/ChinmayK0607/Micromouse/assets/114411195/ec0dbd74-119c-4425-928d-b187f86c4505)


## Hardware Explanation
Here is a both high level and low level diagram for understanding of the hardware implementation
![image](https://github.com/ChinmayK0607/Micromouse/assets/114411195/6be8035b-0604-475b-956f-26d8a51b0aa2)

![image](https://github.com/ChinmayK0607/Micromouse/assets/114411195/b1fa66ec-f1b0-48fe-924e-58f44655b7bf)


The circuit overall is controlled by the Arduino nano. 

The code for movement and speed control as well for maintaining a particular distance from the wall is uploaded in the Arduino nano.
It analyzes the data sent by the motor encoders and calculates the distance covered accordingly. 

It also reads the data from all the three ultrasonic sensors and gives output to the motor so that the bot maintains a particular distance from the wall.

The motor driver receives the input from the Arduino nano and accordingly supplies the signal to the motor so that the motor can perform the required movement.

The circuit drives its power from a 7.4V LiPo batttery.

The connections of the circuit are as shown in the circuit digram above.


## Software Explanation

Since the initial simulations were in python, we had to create data structures for the maze map and directions. We implemented flood fill as the final algorithm as it was the fastest comparitively and gave good results.

How it works:
The flood fill is an optimistic search algorithm that can help in solving mazes, it simulates water flooding a maze and reaching the goal and thus the name. 

It initially assumes that there are no walls and generates a first maze map using bfs/dfs. A maze map considers the goal as 0 and each preceding cell has value one more than the earlier cell.

Example : ``` current_cell.value() = previous_cell.value()+1 ; ```

Flood fill video:

![Untitled video - Made with Clipchamp (5)](https://github.com/ChinmayK0607/Micromouse/assets/114411195/2238fc76-befa-4fdc-a332-68aed780f492)




The mouse then runs once to generate a maze map according to intial run.
It then backtracks using a different path and then decides the shortest path based on these two runs.

Link to extensive breakdown of code: https://hackmd.io/@l_WDq7lkQq29Pz-KD1JPNA/HkYDExRTh


## How to run the code
Download the arudino ide and run the files.

For simulation:
``` pip install pyamaze```

Then you are good to go
