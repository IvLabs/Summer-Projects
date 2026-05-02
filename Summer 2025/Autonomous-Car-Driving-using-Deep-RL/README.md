![Mountain Track Demo](https://raw.githubusercontent.com/tahamm786/Autonomous-Car-Driving-using-Deep-RL/main/Media/Mountain_Track.gif)

# Autonomous Driving Using Deep Reinforcement Learning  
A complete end-to-end DRL system for lane-following in the DonkeyCar simulator.

---

# Objective

The objective of this project is to train an autonomous vehicle to navigate a simulated environment by following lanes, maintaining stability, and controlling speed using Deep Reinforcement Learning (DRL).  
The agent learns directly from raw RGB camera images, which are processed using a CNN-based policy trained with Proximal Policy Optimization (PPO) in the gym-donkeycar environment.

---

# Approach

The development of the final driving agent followed a structured multi-stage approach.

## 1. Reinforcement Learning Fundamentals  
Before moving to a vision-based DRL setup, foundational RL algorithms were implemented and studied in detail.  
This included value iteration, policy iteration, Monte Carlo methods, Temporal-Difference learning (SARSA, Q-learning), and exploration strategies.  
These were implemented in environments like FrozenLake and MiniGrid to build intuition about agent learning and policy behavior.

![Classical RL tasks](https://raw.githubusercontent.com/tahamm786/Autonomous-Car-Driving-using-Deep-RL/main/Media/frozen_lake.gif)

---

## 2. Neural Network and Deep Learning Foundations  
To prepare for working with image-based inputs, neural networks were implemented from scratch using NumPy (forward and backward propagation), followed by CNNs and deep learning models in TensorFlow.  
This provided the necessary understanding of spatial feature extraction, which is essential for lane detection and driving behavior.

---

## 3. Transition to Deep Reinforcement Learning  
After developing the basics, policy-gradient algorithms and Actor-Critic methods were studied.  
This formed the theoretical backbone for implementing PPO and understanding why it is well suited for continuous control.

![Policy Gradient diagram](https://raw.githubusercontent.com/tahamm786/Autonomous-Car-Driving-using-Deep-RL/main/Media/policy_gradient.jpg)

---

## 4. Building the Autonomous Driving Agent  
The final model integrates three core components:

- DonkeyCar simulator for environment interaction  
- CNN feature extractor for visual observations  
- PPO-based Actor-Critic architecture for action selection and value estimation  

The agent learns to control steering and throttle using feedback from a reward function designed to encourage stable, centered driving.

![Driving pipeline diagram](https://raw.githubusercontent.com/tahamm786/Autonomous-Car-Driving-using-Deep-RL/main/Media/driving_pipeline.png)

---

# Environment: gym-donkeycar

### Action Space (Continuous)

| Action    | Range     |
|-----------|-----------|
| Steering  | -5 to +5  |
| Throttle  | 0 to 1    |

### Observation Space  
- 120×160 RGB camera frame  
- Contains road edges, curvature, and background context  
- Used as direct input to the CNN network  

![CAMERA FRAME](https://raw.githubusercontent.com/tahamm786/Autonomous-Car-Driving-using-Deep-RL/main/Media/camera_view.png)

### Reward Function  
The reward encourages smooth and safe driving:

- Strong penalties for collisions  
- Penalties for going off-track (max cross-track error reached)  
- Positive reward proportional to centeredness and forward velocity  

This motivates the agent to balance both lateral stability and speed.

![Reward function chart](https://raw.githubusercontent.com/tahamm786/Autonomous-Car-Driving-using-Deep-RL/main/Media/reward_fn.png)

---

# Proximal Policy Optimization (PPO)

PPO is the reinforcement learning algorithm used to train the driving agent.  
It is well suited for continuous control problems like steering and throttle regulation.

PPO follows an Actor-Critic design:

### Actor
- Receives CNN features  
- Outputs continuous steering and throttle  
- Represents the policy that selects actions

### Critic
- Estimates the value of the current state  
- Helps guide policy updates through advantage estimation  

---

## Why PPO Works Well for Driving

Driving requires stable, incremental learning because sudden policy changes lead to crashes or inconsistent behavior.  
PPO addresses this through three main ideas:

### 1. Clipped Objective  
PPO restricts how much the new policy can deviate from the old policy during updates.  
This prevents unstable jumps in behavior and keeps training controlled and reliable.

### 2. Efficient Advantage Estimation  
Generalized Advantage Estimation (GAE) is used to compute how much better a chosen action was compared to expected performance.  
This results in smoother and more informative updates.

### 3. Sample Efficiency  
PPO reuses collected experiences multiple times via mini-batch optimization, making training more efficient while preserving stability.

---

## Summary of PPO in This Project  
- CNN extracts lane-related features from camera frames  
- Actor outputs continuous control commands  
- Critic estimates long-term future reward  
- PPO updates the policy gradually using clipped ratios  
- Training remains stable across thousands of steps  

This combination allows the agent to learn consistent and robust driving behavior from visual input alone.

---

# Algorithm Pipeline (Step-by-Step)

1. Capture camera frame  
2. Preprocess and pass through CNN  
3. Extract features  
4. Actor produces steering and throttle  
5. Environment applies the action  
6. Reward and next state are returned  
7. Transition stored in rollout buffer  
8. PPO performs policy and value updates  
9. Loop continues across many timesteps  

![ALGO PIPELINE](https://raw.githubusercontent.com/tahamm786/Autonomous-Car-Driving-using-Deep-RL/main/Media/algo_pipeline.png)

---

# Training and Results

### Learning Progress  
- Early stages: frequent off-track events  
- Mid training: better lane centering, improved curvature handling  
- Final stages: smooth lane-following with stable throttle control  

![Generated Road Final](https://raw.githubusercontent.com/tahamm786/Autonomous-Car-Driving-using-Deep-RL/main/Media/DonkeyCar2.gif)

### Mountain Track Generalization  
A more challenging test track with sharp turns and elevation.  
The trained agent adapts and navigates reliably after extended training.

![Mountain Track Demo](https://raw.githubusercontent.com/tahamm786/Autonomous-Car-Driving-using-Deep-RL/main/Media/Mountain_Track.gif)
![Mountain Track Graph](https://raw.githubusercontent.com/tahamm786/Autonomous-Car-Driving-using-Deep-RL/main/Media/mountain_track_rewards.png)

---

# Project Outcomes

The trained agent successfully:

- Maintains lane position  
- Controls speed effectively  
- Completes full laps without intervention  
- Learns solely from raw camera input  
- Uses PPO for stable and robust continuous control  

---

# Trained Models and Video Results

https://drive.google.com/drive/folders/1XSjvIME7LpQvYnJbaveoxq4y3vlnoDG8?usp=drive_link

---

# Real-World Use Cases

- **Autonomous Vehicles:** Lane-following, speed control, and safe navigation using camera-based policies.  
- **Robotics:** Path planning and real-time control for mobile robots in warehouses and factories.  
- **Smart Transportation:** Traffic optimization, adaptive cruise systems, and intelligent lane assistance.  
- **Sim-to-Real Transfer:** Safe training in simulators before deploying in physical environments.  
- **Drones:** Stable autonomous flight, navigation, and environment-aware control.  
- **ADAS Systems:** Vision-based alerts, steering assistance, and driver-support features.  
- **Research & Education:** Benchmarking RL algorithms and studying vision-based continuous control.

---
