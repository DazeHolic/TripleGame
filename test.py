from triple_game import TripleEnv
import time
import random

env = TripleEnv()
obs = env.reset()
for _ in range(1000000):
    obs, award, end, _ = env.step(random.randint(0, 6), random.randint(0, 6), random.randint(0, 3))  # take a random action
    env.render()
    #time.sleep(1)
    if end:
        env.reset()
env.close()
