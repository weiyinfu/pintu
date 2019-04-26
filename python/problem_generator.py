import numpy as np
import random


def random_pintu(xsize, ysize):
    a = np.arange(0, xsize * ysize).reshape(xsize, ysize)
    # 为确保有解，进行打乱
    for i in range(xsize):
        for j in range(ysize):
            a[i][j] = (a[i][j] + 1) % (xsize * ysize)
    space = xsize - 1, ysize - 1
    for i in range(xsize * ysize * 16):
        di = random.choice([(0, 1), (0, -1), (-1, 0), (1, 0)])
        x, y = space[0] + di[0], space[1] + di[1]
        if xsize > x >= 0 and ysize > y >= 0:
            a[x, y], a[space[0], space[1]] = a[space[0], space[1]], a[x, y]
            space = x, y
    return a
