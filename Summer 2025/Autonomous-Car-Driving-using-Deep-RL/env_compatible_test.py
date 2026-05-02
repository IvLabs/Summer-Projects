import gym
from donkey_env import GeneratedRoadsEnv , MountainTrackEnv
from stable_baselines3 import PPO
 # replace with your env

# Create instances
env1 = GeneratedRoadsEnv()
env2 = MountainTrackEnv()

# Now check action and observation spaces
print("Action space match:", env1.action_space == env2.action_space)
print("Observation space match:", env1.observation_space == env2.observation_space)
