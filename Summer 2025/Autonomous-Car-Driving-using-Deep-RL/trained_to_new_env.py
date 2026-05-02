import gymnasium as gym
from donkey_env import GeneratedRoadsEnv ,GeneratedTrackEnv,WarehouseEnv,MountainTrackEnv
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import VecTransposeImage,DummyVecEnv
from stable_baselines3.common.vec_env import VecNormalize
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.callbacks import BaseCallback
import matplotlib.pyplot as plt
import pandas as pd  # for rolling average
from gymnasium.wrappers import RecordEpisodeStatistics
from wrapper import CustomRewardWrapper


# --- Config ---
port = 9091
conf = {
    "exe_path": "None",
    "port": port,
    "frame_skip": 1,
    "time_step": 0.1,
    "camera_width": 80,
    "camera_height": 60,
    "camera_depth": 3,
    "log_level": 20,
    "render": False,
    "lidar": True,
    "headless": True,
}

# --- New Environment (MountainTrack) ---
def make_env():
    env = MountainTrackEnv(conf=conf)
    
    return env

env = DummyVecEnv([make_env])
env = VecTransposeImage(env)
env = VecNormalize(env, norm_obs=False, norm_reward=True, clip_obs=10.)

# --- Load Pretrained Model (from GeneratedRoads) ---
model = PPO.load(r"C:\Users\HP\OneDrive\Desktop\SUMMER_INTERN_IVLABS\DonkeyCar\ppo_ALL1.zip",env=env, device="cuda")

model.learning_rate = 3e-4  # or even 5e-4 for short adaptation


# --- Continue Training ---
model.learn(
    total_timesteps=10000,
    progress_bar=True,
    reset_num_timesteps=False,
    tb_log_name="GeneratedRoadsEnv_cnn_finetune",
    log_interval=100
)

# --- Save New Model ---
model.save("ppo_ALL1")

env.close()
