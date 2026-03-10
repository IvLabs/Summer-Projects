# **Gesture Controlled Quadcopter**

## **Table of Contents** 
- [**Gesture Controlled Quadcopter**](#gesture-controlled-quadcopter)
  - [**Table of Contents:**](#table-of-contents)
  - [**Objective**](#objective)
  - [**Gesture Recognisation**](#gesture-recognisation)
  - [**Command Maping and Forwarding**](#command-maping-and-forwarding)
  - [**Setup's and Running**](#setup-and-running)
    - [**SITL Setup**](#sitl-setup)
      - [**Ground Control Station**](#ground-control-station)
      - [**Ubuntu 22.04.5 LTS**](#ubuntu-22045-lts)
      - [**Python 3.10.11**](#python-31011)
      - [**Ardupilot**](#ardupilot)
      - [**Configure ArduPilot Firmware**](#configure-ardupilot-firmware)
    - [**Gazeebo Setup**](#gazeebo-setup)
      - [**ArduCopter**](#arducopter)
      - [**ArduCopter Gazebo Plugin**](#arducopter-gazebo-plugin)
    - [**Simulation Run**](#simulation-run)
  - [**Test Flight Result**](#test-flight-result)
      


## **Objective**
Our goal is to develop an advanced drone capable of autonomous flight, seamlessly responding to gesture-based commands from a ground-based pilot. The drone will interpret and execute these commands with precision, enabling dynamic and user-friendly control for a range of applications.

Implement wireless communication protocols to transmit precise gesture-based commands from a Ground Control Station (GCS) to the drone.

## **Gesture Recognisation** 
![Gestures Recognisation](./thumbnails/index.png)

- Gesture recogntion is done using training a ML model on a dataset containing labelled distances between all possible pair of hand landmarks
- The loading hand landmarks and extraction of their x,y,z coordinates are done using mediapipe library
- RandomForestClassifier is the ML model used in training

Approach for Data colection

- Using mediapipe we extract the features of each hand landmark(i.e. it's x,y,z coordinates)
- Then for all possible pairs of hand landmarks i.e. C(21,2) = 210 pairs distances between them are calculated and stored in a labelled CSV dataset respective to a particular gesture
- Also, before storing them we divide the distances by width of the user's hand (Distance between landmark 5 and 17), this is done so that our model is relative and not just trained according to one person only
- Now, for each gesture we collect 5k rows of 210 distance data (this is done for better training), colletion speed is 10rows/sec
- Now, when the dataset is ready for all the gesture we move to the training part


Model training 

- The training script will load the CSV file, it will label the string(like "takeoff") and will map them to integers
- Then the data will me randomised and it will be split into 80% training data and 20% testing data
- Now, using StandardScalar for every feature, mean = 0 and standard deviation = 1 is set, it will prevent imbalance in feature distribution
- RandomForestClassifier is the ML model which is trained with parameters like 300 Decision trees, tree depth limit as 20
- The model is evaluated using classification report and heatmap confusion matrix
- While evaluating, the threshold is set as 0.8, so if probability while testing is <0.8 it is treated as 'unknown'
- Once trained and evaluated, the model in saved in .pkl file format which is the used for prediction

![gestures](./thumbnails/gestures.png)



## **Command Maping and Forwarding**
![commands](https://github.com/aman-59/Gesture-Controlled-Quadcopter/blob/main/thumbnails/command.png)
- Our final script has 2 parts 
    1. Drone command excecution code / Connection code
    2. Gesture recognition code
- Before running the code, Using Mavlink the mavproxy commands are forwarded to 2 udp ports, one connects to Mission Planar and the other connects to connection python code
- Then the connection code is run it connects to the vehicle, performs all security checks and using multithreading creates a seperate thread in which gesture recogntion code runs
- The seperation of tasks ensures stability, and prevents any potential crash or command delays
- The recognition code continiously detects and sends gesture to command excecution code which stores it in a deque of size 15(first-in-last-out format)
- Best stable gesture is the one whose occurance is more than 70% in the deque, it is selected and it's respective mavproxy command is forwarded, this adds stability and prevents any fluctuation in gesture recognition which can lead to potential crash
- There are two safety checks added, first being that during change in stable gesture the drone pauses and waits for 1.5 seconds, also before land command is forwarded it is ensured that stable gesture is land for atleast 5 seconds




## **Setup and Running**
### **SITL Setup**
Install Requirements: 
#### **Ground Control Station**
 Mission Planner: https://ardupilot.org/planner/docs/mission-planner-installation.html#windows-installation 
#### **Ubuntu 22.04.5 LTS**
https://releases.ubuntu.com/jammy/
#### **Python 3.10.11**

```
sudo apt install -y software-properties-common build-essential zlib1g-dev \
libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev \
libffi-dev libsqlite3-dev wget libbz2-dev
```
```
cd /tmp    
wget https://www.python.org/ftp/python/3.10.11/Python- 3.10.11.tgz
```

```
tar -xvf Python-3.10.11.tgz
cd Python-3.10.11
```

```
 ./configure --enable-optimizations
```

```
make -j$(nproc)
sudo make altinstall
```

#### **ArduPilot** 
Run the following commands to clone the official GitHub Repo of ArduPilot.
```
git clone https://github.com/ArduPilot/ardupilot.git
cd ardupilot
git submodule update --init --recursive
```
Run the Following Commands inside the ardupilot directory
```
cd Tools/environment_install
./install-prereqs-ubuntu.sh
```
Follow the Default Installation Instructions.
Wait till installation to complete.
This step will create a virtual enviornment (venv-ardupilot) in Home Directory where all the dependencies Would be install.

#### **Configure ArduPilot Firmware**
:warning: Activate the Virtual Enviornment Before Running These Coommands.
Move to ardupilot Directory before running the following commands
```
./waf configure --board sitl
```
```
./waf copter
```

Test Run:

```
./Tools/autotest/sim_vehicle.py -v ArduCopter --console 

```
Restart the terminal and try running sim_vehicle.py

### **Gazeebo Setup** 
#### **ArduCopter** 
SITL Supports Gazebo Harmonic (Outdated as of now but works well)
Run this instructions in the order
 Exit Virtual Enviornment Before this Setup
 
```
sudo apt-get update
sudo apt-get install curl lsb-release gnupg 
```

```
sudo curl https://packages.osrfoundation.org/gazebo.gpg --output /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null
sudo apt-get update
sudo apt-get install gz-harmonic
```

#### **ArduCopter Gazebo Plugin**
```
sudo apt update
sudo apt install libgz-sim8-dev rapidjson-dev
sudo apt install libopencv-dev libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev gstreamer1.0-plugins-bad gstreamer1.0-libav gstreamer1.0-gl
```
```
mkdir -p gz_ws/src && cd gz_ws/src
git clone https://github.com/ArduPilot/ardupilot_gazebo
```
```
export GZ_VERSION=harmonic
cd ardupilot_gazebo
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=RelWithDebInfo
make -j4
```
```
echo 'export GZ_SIM_SYSTEM_PLUGIN_PATH=$HOME/gz_ws/src/ardupilot_gazebo/build:${GZ_SIM_SYSTEM_PLUGIN_PATH}' >> ~/.bashrc
echo 'export GZ_SIM_RESOURCE_PATH=$HOME/gz_ws/src/ardupilot_gazebo/models:$HOME/gz_ws/src/ardupilot_gazebo/worlds:${GZ_SIM_RESOURCE_PATH}' >> ~/.bashrc
```


### **Simulation Run**

Run all the applications in order all in new terminal. 
1. Gazebo 
2. ArduCopter
3. Command Script

```
gz sim -v4 -r iris_runway.sdf
```
```
sim_vehicle.py -v ArduCopter -f gazebo-iris --model JSON
```

```
git clone https://github.com/aman-59/Gestured-Controlled-Quadcopter.git
cd Gestured-Controlled-Quadcopter
python3 quad.py
```



## **Test Flight Result**
<table>
  <tr>
    <td align="center">
      <h4>Forward</h4>
      <img src="media/forward.gif" alt="Forward Gesture" width="100%">
    </td>
    <td align="center">
      <h4>Backward</h4>
      <img src="media/backward.gif" alt="Backward Gesture" width="100%">
    </td>
    <td align="center">
      <h4>Left</h4>
      <img src="media/left.gif" alt="Left Turn Gesture" width="100%">
    </td>
  </tr>
  <tr>
    <td align="center">
      <h4>Right</h4>
      <img src="media/right.gif" alt="Right Turn Gesture" width="100%">
    </td>
    <td align="center">
      <h4>LAND</h4>
      <img src="media/land.gif" alt="Land Gesture" width="100%">
    </td>
    <td width="33%">
      </td>
  </tr>
</table>
