import gym
import numpy as np
from gymnasium import RewardWrapper
import numpy as np


class CustomRewardWrapper(gym.Wrapper):
    def __init__(self, env):
        super().__init__(env)

    def step(self, action):
        obs, reward,done, info = self.env.step(action)

        # Extract simulator info
        donkey_info = info.get("donkey", {})
        cte = donkey_info.get("cte", 0.0)     # Cross track error
        speed = donkey_info.get("speed", 0.0) # Vehicle speed
 
        # --- Reward Shaping ---
        # Base reward: forward speed
        new_reward = speed * 0.1  

        # Symmetric center penalty (cte^2 avoids left/right bias)
        new_reward -= (cte ** 2) * 0.05  

        # Bonus for staying very close to center
        center_bonus = max(0, 1.0 - abs(cte))
        new_reward += 0.2 * center_bonus

        # Encourage smoother driving by punishing extreme steering
        steer = action[0] if isinstance(action, (list, tuple)) else 0.0
        new_reward -= 0.1 * (steer ** 2)

        # Small survival reward
        new_reward += 0.05  

        return obs, new_reward, done, info
