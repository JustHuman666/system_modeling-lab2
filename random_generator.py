import random
import numpy as np

def exponential(time_mean):
    a = 0.0
    while a == 0:
        a = random.random()
    a = -time_mean * np.log(a)
    return a

def normal(time_mean, time_deviation):
    return time_mean + time_deviation * random.gauss(0.0, 1.0)

def uniform(time_min, time_max):
    a = 0.0
    while a == 0:
        a = random.random()
    a = time_min + a * (time_max - time_min)
    return a


