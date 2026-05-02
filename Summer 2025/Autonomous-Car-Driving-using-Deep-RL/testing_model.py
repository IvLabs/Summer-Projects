import gymnasium as gym 
from donkey_env import GeneratedRoadsEnv , CircuitLaunchEnv , GeneratedTrackEnv, WarehouseEnv , MountainTrackEnv
from stable_baselines3 import PPO
from stable_baselines3.common.vec_env import VecTransposeImage, DummyVecEnv


# --- DonkeyCar config ---
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
    "render": True,   # 👈 Turn ON rendering for testing
    "lidar": True,
    "headless": False,  # 👈 disable headless so you can see the run
}

# --- Environment ---
def make_env():
    env = MountainTrackEnv(conf=conf)
    return env

env = DummyVecEnv([make_env])
env = VecTransposeImage(env)

# --- Load trained PPO model ---
model = PPO.load(r"C:\Users\HP\OneDrive\Desktop\SUMMER_INTERN_IVLABS\DonkeyCar\ppo_Mountain_GeneratedRoads.zip", env=env, device="cuda")  # or "cpu"

# --- Evaluation ---
episodes = 3
for ep in range(episodes):
    obs = env.reset()
    done = False
    total_reward = 0


    while not done:
        action, _ = model.predict(obs, deterministic=True)
        obs, reward,done,info = env.step(action)
        total_reward += reward

        

    print(f"Episode {ep+1}: total reward = {total_reward}")
    

env.close()
