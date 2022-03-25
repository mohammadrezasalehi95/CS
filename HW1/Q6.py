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

arrival_times = [0 for _ in range(2000)]
for i in range(1, 2000):
    arrival_times[i] = interval_time[i - 1] + arrival_times[i - 1]

group_arrival_time = [0 for i in range(400)]
for i in range(400):
    group_arrival_time[i] = arrival_times[i * 5 + 4]

# game time random calc
game_time = [random.choices(
    [20, 18, 16, 14, 12],
    weights=[0.09, 0.14, 0.16, 0.26, 0.35],
    k=1)[0] for i in range(400)]

game_begins = [0 for i in range(400)]
game_ends = [0 for i in range(400)]
game_land_0 = []
game_land_1 = []
# game calculation
game_begins[0] = group_arrival_time[0]
game_ends[0] = game_begins[0] + game_time[0]
game_land_0.append([game_begins[0], game_ends[0], 0])
game_begins[1] = group_arrival_time[1]
game_ends[1] = game_begins[1] + game_time[1]
game_land_1.append([game_begins[1], game_ends[1], 1])

for i in range(2, 400):
    min_end_game_land = min(game_land_0, game_land_1, key=lambda a: a[-1][1])
    game_begins[i] = max(group_arrival_time[i], min_end_game_land[-1][1])
    game_ends[i] = game_begins[i] + game_time[i]
    min_end_game_land.append([game_begins[i], game_ends[i], i])

# results


# customers waiting time in queue

slots_waiting = [mean([game_begins[i] - arrival_times[i * 5 + j] for i in range(400)]) for j in range(5)]
print("overall mean", mean(slots_waiting))
print("mean by slot in order", slots_waiting)

# customer spending time
spends_time = [game_ends[i // 5] - arrival_times[i] for i in range(2000)]

print("spending time mean", mean(spends_time))

# game utilization
idle_time_games = [game_begins[i] - game_ends[i - 1] for i in range(1, 400)]
idle_time_land_0 = [game_land_0[0][0]] + [game_land_0[i][0] - game_land_0[i - 1][1] for i in range(1, len(game_land_0))]
idle_time_land_1 = [game_land_1[0][0]] + [game_land_1[i][0] - game_land_1[i - 1][1] for i in range(1, len(game_land_1))]

print("land 1 utilization percent", (game_land_0[-1][1] - sum(idle_time_land_0)) / game_land_0[-1][1] * 100)
print("land 2 utilization percent", (game_land_1[-1][1] - sum(idle_time_land_1)) / game_land_1[-1][1] * 100)

# queue average

event_table = {'Events': [], 'Time': []}
for arrival_time in arrival_times:
    event_table['Events'].append('A'),
    event_table['Time'].append(arrival_time)
for game_begin in game_begins:
    event_table['Events'].append('D'),
    event_table['Time'].append(game_begin)
event_table = pd.DataFrame.from_dict(event_table)
event_table = event_table.sort_values(by=['Time'])

number_in_queue = 0
last_event_time = 0
cumulative_queue_time = 0
for i, row in event_table.iterrows():
    cumulative_queue_time += (row['Time'] - last_event_time) * number_in_queue
    if row['Events'] == 'A':
        number_in_queue += 1
    else:
        number_in_queue -= 5
    last_event_time = row['Time']

print("queue waiting average length", cumulative_queue_time / last_event_time)

# slot waiting mean will decrease by adding land
# spending time in game and queue will decrease by adding land
# land utilization will decrease by adding land (land idle time will increase)
# queue waiting length will decrease by adding land
