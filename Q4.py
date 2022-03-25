import random
import numpy as np

random.seed(200)
print("interval time")
for i in range(9):
    print(random.choice(
        random.choices(
            [(9, 10, 11, 12, 13, 14), (6, 7, 8), (3, 4, 5), (1, 2)],
            weights=[0.24, 0.17, 0.34, 0.25],
            k=1
        )[0]))
print("service time")
for i in range(10):
    print(random.choice(
        random.choices(
            [(9, 10, 11, 12), (6, 7, 8), (4, 5), (1, 2, 3)],
            weights=[0.34, 0.26, 0.24, 0.15],
            k=1
        )[0]))
