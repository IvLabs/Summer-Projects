# Snake game AI

#### Created in [Gym-Snake](https://github.com/grantsrb/Gym-Snake.git) environment.

## Description
![](https://i.imgur.com/DLDVj7C.gif)

This is an attempt to solve classic snake game using Reinforcement learning method i.e Q-learning.

## Implementation

### Action Space

The action space consists of 4 actions -

	UP    - 0
	RIGHT - 1
	DOWN  - 2
	LEFT  - 3
	
All the actions and directions are absolute to the environment, but for the agent these actions made relative with respect to the head of the snake so as to correspond to the state space. They are related by following relation-

New relative actions-
	
	LEFT     -  d-1
	RIGHT    -  d+1
	FORWARD  -  d 
	BACKWARD -  abs(d-2)
    
Where `d` is the direction of the snake's head. All the exceptions are handled for a particular direction. For example - if the head is facing `UP`, so relatively `LEFT` action must be `3` not `-1`. Similarly other exceptions are handled.

### State Space

A state is defined by 4 parameters, these are

	a) Relative direction of the food - 4
	b) Presence of obstacle or border immediately to the left of the snake head - 2 (0 or 1)
	c) Presence of obstacle or border immediately to the right of the snake head
	d) Presence of obstacle or border in front of the snake head

This establishes a state space that has (4 x 2 x 2 x 2) = 32 states

These aren't enough to completely solve the game, but it learns how to play decently.

### Reward function

* +1 for eating the food
* -1 for hitting with wall or its body

Except above two conditions by default value of reward function is 0.

### Algorithm

Off-policy learning method, namely Q-learning is used to train agent. While following it's behaviour policy μ(a|s), it evaluates optimal policy π(a|s) to get optimal Q(s,a) values.

## Results

### Training

![](https://i.imgur.com/BUzFVQv.png)

### Testing

![](https://i.imgur.com/lqs13Rz.png)

## Limitations

* With this approach optimal policy cannot be obtained because the snake's obstacle dodging logic can dodge only immediate obstacles.
* Since the agent can only see its immediate obstacles, there are high possibilities of the agent being entangled in a loop which results in death after few steps.
* The state space is not large enough to derive an optimal policy for the game using Tabular Methods (A very large state space will be required if one was to attempt to use tabular method to find an optimal policy).
* The state space cannot be generalized for all states of the environment.

## Multisnake Environment

We trained the snake in a solo world, then got the policy from it and fed it into the  individual snakes of this multi snake environment.

![](https://i.imgur.com/qSTImYz.gif)

Run `2Snake.py` to have 2 Agents play the game simultaneously and `3Snake.py` to have 3 Agents.

![](https://i.imgur.com/41RV94Z.gif)

## Walled Environment

To add walls make changes in the `snake/env.py` file and execute the `SnakeAI.py`

![](https://i.imgur.com/DA7xWzZ.gif)

# Environment

#### Created in response to OpenAI's [Requests for Research 2.0](https://blog.openai.com/requests-for-research-2/)

## Description
gym-snake is a multi-agent implementation of the classic game [snake](https://www.youtube.com/watch?v=wDbTP0B94AM) that is made as an OpenAI gym environment.

The two environments this repo offers are snake-v0 and snake-plural-v0. snake-v0 is the classic snake game. See the section on SnakeEnv for more details. snake-plural-v0 is a version of snake with multiple snakes and multiple snake foods on the map. See the section on SnakeExtraHardEnv for more details. 

Many of the aspects of the game can be changed for both environments. See the Game Details section for specifics.

## Dependencies
- pip
- OpenAI Gym
- NumPy
- Matplotlib

## Installation
1. Clone this repository
2. Navigate to the cloned repository
3. Run command `$ pip install -e ./`
