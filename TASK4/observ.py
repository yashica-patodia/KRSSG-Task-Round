import gym
env = gym.make("Pendulum-v0")
import time 

while True:
    obs = env.reset()
    done = False
    global total
    total=0
    while not done:
        # in practice the action comes from your policy
        action = env.action_space.sample()
	
        obs, rew, done, misc = env.step(action)
        total+=rew
        print(obs,rew)
        env.render()
    print(total)
    time.sleep(2)
