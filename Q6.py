import random
from statistics import mean

import numpy as np
import pandas as pd

random.seed(200)
# interval time random calc
interval_time = [random.choices(
    [3, 2, 1],
    weights=[0.19, 0.51, 0.3],
    k=1)[0] for i in range(1999)]

arrival_time = [0 for _ in range(2000)]
for i in range(1, 2000):
    arrival_time[i] = interval_time[i - 1] + arrival_time[i - 1]

group_arrival_time = [0 for i in range(400)]
for i in range(400):
    group_arrival_time[i] = arrival_time[i * 5 + 4]

# game time random calc
game_time = [random.choices(
    [20, 18, 16, 14, 12],
    weights=[0.09, 0.14, 0.16, 0.26, 0.35],
    k=1)[0] for i in range(400)]

game_begins = [0 for i in range(400)]
game_ends = [0 for i in range(400)]
# game calculation
game_begins[0] = group_arrival_time[0]
game_ends[0] = game_begins[0] + game_time[0]
for i in range(1, 400):
    game_begins[i] = max(group_arrival_time[i], game_ends[i - 1])
    game_ends[i] = game_begins[i] + game_time[i]

# results


# customers waiting time in queue

slots_waiting = [mean([game_begins[i] - arrival_time[i * 5 + j] for i in range(400)]) for j in range(5)]
print("overall mean", mean(slots_waiting))
print("mean by slot in order", slots_waiting)

# customer spending time
spends_time = [game_ends[i // 5] - arrival_time[i] for i in range(2000)]

print("spending time mean", mean(spends_time))


# game utilization
idle_time_games = [game_begins[i] - game_ends[i - 1] for i in range(1, 400)]

print("game utilization percent", (game_ends[-1] - sum(idle_time_games)) / game_ends[-1] * 100)

# queue average