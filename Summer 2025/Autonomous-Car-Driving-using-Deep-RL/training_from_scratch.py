import gymnasium as gym
from donkey_env import WarehouseEnv , MountainTrackEnv , GeneratedRoadsEnv
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import VecTransposeImage,DummyVecEnv, VecNormalize

prev_steer = 0


port=9091
# --- DonkeyCar config ---
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

# ----------------------------
# Environment creation
# ----------------------------
def make_env():
    env = GeneratedRoadsEnv(conf=conf)
    return env

env = DummyVecEnv([make_env])
env = VecTransposeImage(env)              # for CNN policies
env = VecNormalize(env, norm_obs=False, norm_reward=True, clip_obs=10.)

# ----------------------------
# Create PPO model
# ----------------------------
model = PPO(
    "CnnPolicy",
    env,
    learning_rate=1e-4,
    verbose=1,
    device="cuda",
    tensorboard_log="./logs/"
)

# ----------------------------
# Train from scratch
# ----------------------------
model.learn(
    total_timesteps=15000,
    progress_bar=True,
    tb_log_name="GeneratedRoadsEnv_cnn_finetune",
    log_interval=100
)

# ----------------------------
# Save model and normalization stats
# ----------------------------
model.save("log.zip")
env.save("vecnormalize_GeneratedRoadsEnv.pkl")  # save normalization stats for future fine-tuning

env.close()
print("Training complete and model saved.")