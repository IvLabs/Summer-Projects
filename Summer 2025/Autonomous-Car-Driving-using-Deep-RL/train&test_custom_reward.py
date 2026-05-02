import gym
from donkey_env import GeneratedRoadsEnv 
from stable_baselines3 import PPO
from wrapper import CustomRewardWrapper


prev_steer = 0

def custom_reward(observation, action, done, info):
    global prev_steer
    steer, throttle = action  

    # Simulator info
    cte = info.get("cte", 0.0)     # cross-track error
    speed = info.get("speed", 0.0) # current speed
    hit = info.get("hit", False)   # crash flag

    # 1) Reward staying near the center (main driver)
    reward_centering = 5.0 - abs(cte)   # best if cte ~ 0
    reward_centering = max(reward_centering, -1.0)  # don’t let it blow up negative

    # 2) Reward speed, but only if close to center
    if abs(cte) < 1.5:  
        reward_speed = 0.3 * speed     # higher speed → more reward
    else:
        reward_speed = 0.0             # ignore speed if drifting away

    # 3) Small survival bonus (keeps it alive)
    reward_alive = 0.1

    # 4) Smooth driving: penalize jerky and large steering
    smoothness = -0.2 * abs(steer - prev_steer) - 0.05 * abs(steer)

    # 5) Crash penalty
    crash_penalty = -10.0 if hit else 0.0

    # Update prev_steer
    prev_steer = steer if not done else 0.0

    # Total reward
    reward = reward_centering + reward_speed + reward_alive + smoothness + crash_penalty

    return reward



#exe_path = "DonkeySimWin/donkey_sim.exe"  # Update this path if needed
port = 9091

conf ={
    "exe_path": "None",
    "port": port,
    "frame_skip": 1,
    "time_step": 0.1,
    "camera_width": 80,
    "camera_height": 60,
    "camera_depth": 3,
    "log_level": 20,
    "render": False,
    "lidar":True,
    "headless": True,}

env = GeneratedRoadsEnv(conf=conf)
env= CustomRewardWrapper(env,custom_reward)


model=PPO('MlpPolicy',
    env,
    verbose=1,
    tensorboard_log='logs',
    learning_rate=0.01,        
    n_steps=2048,              
    batch_size=64,            
    n_epochs=10,               
    gamma=0.995,               
    gae_lambda=0.95,          
    clip_range=0.25,            
    ent_coef=0.02,            
    policy_kwargs={'net_arch': [128, 128]},  
    device='cuda',
)

model.learn(total_timesteps=100000,
            progress_bar=True,
            reset_num_timesteps=False,
            tb_log_name="donkeycar_1",
            log_interval=10)

model.save("ppo_donkeycar")

episodes = 10
for ep in range(episodes):
    obs = env.reset()
    done = False
    total_reward = 0
    
    while not done:
        action, _ = model.predict(obs, deterministic=True) 
        obs, reward, done, info = env.step(action)
        total_reward += reward
    
    print(f"Episode {ep+1}: total reward = {total_reward}")

env.close()
