import queue
import time

import numpy  as np

import problem_generator

"""
最小的拼图：2*2
分为三部分：左上角xsize-2*ysize-2的拼图，左边的2列，下面的两行
本程序的瓶颈在于寻路函数：即给定源点和目标点，
在不经过某些点的情况下找到一条尽量近的路径，广搜不是最好的方法
"""
xsize = 3  # 行数
ysize = 3  # 列数
a = np.arange(0, xsize * ysize).reshape(xsize, ysize)  # 拼图数组
where = None  # [(-1, -1)] * (xsize * ysize)  # 存储位置信息，便于快速定位
ready_flag = [[0] * ysize for _ in range(xsize)]  # 标识此块是否已经拼好，已经拼好就不能再动了
ans_op = ""

directions = [(0, 1), (0, -1), (-1, 0), (1, 0)]  # 右，左，上，下
gold_op = [0, 2, 1, 3, 1, 2, 0, 0, 3, 1]  # 黄金操作，此法可以解决任意2行N列拼图
# gold_op顺时针旋转90度，用于解决N行2列拼图
gold_op_vertical = list(map(lambda x: [3, 2, 0, 1][x], gold_op))


def legal(x, y):
    return xsize > x >= 0 and ysize > y >= 0


def op_to_char(op):
    for i in range(4):
        if op == directions[i]:
            return '右左上下'[i]


def swap_neibor(src, des):
    # 交换相邻的两块
    global ans_op
    if a[src[0], src[1]] == 0: des, src = src, des
    ans_op += op_to_char((des[0] - src[0], des[1] - src[1]))
    a[src[0]][src[1]], a[des[0]][des[1]] = a[des[0]][des[1]], a[src[0]][src[1]]
    where[a[src[0], src[1]]] = src[0], src[1]
    where[a[des[0], des[1]]] = des[0], des[1]
    # print(ans_op, '\n', a)


def where_is(x, y):
    # 应该在（x,y）处的小块现在在哪里
    return where[(x * ysize + y + 1) % (xsize * ysize)]


def init_pos():
    for i in range(xsize):
        for j in range(ysize):
            where[a[i, j]] = (i, j)


def get_path(fx, fy, tx, ty, still_x, still_y):
    # 求一条从f到t的路径并且不能经过still
    distance = np.zeros((xsize, ysize)) - 1  # 距离矩阵
    q = queue.Queue(xsize * ysize)  # 广搜队列
    q.put((fx, fy))  # 把源点入队
    distance[fx, fy] = 0
    last_pos = [[0] * ysize for _ in range(xsize)]  # 记录搜索路径

    def bfs():
        while not q.empty():
            now = q.get()
            for i in directions:
                xx, yy = now[0] + i[0], now[1] + i[1]
                # 要求xx，yy：不能越界，未访问过，不能经过固定点，不能经过已经排好位置的点
                if legal(xx, yy) \
                        and distance[xx][yy] == -1 \
                        and (xx, yy) != (still_x, still_y) \
                        and ready_flag[xx][yy] == False:
                    q.put((xx, yy))
                    distance[xx][yy] = distance[now[0]][now[1]] + 1
                    last_pos[xx][yy] = now
                    if (xx, yy) == (tx, ty):
                        return

    bfs()
    path = []
    i, j = tx, ty
    while 1:
        path.append((i, j))
        if (i, j) == (fx, fy):
            break
        i, j = last_pos[i][j]
    return path[::-1]


def move_space_to(x, y, still_x, still_y):
    # 在保持still_x和still_y静止的条件下把空格移动到x,y
    space_x, space_y = where_is(xsize - 1, ysize - 1)
    path = get_path(space_x, space_y, x, y, still_x, still_y)
    for i in range(1, len(path)):
        swap_neibor(path[i], path[i - 1])


def move(src_x, src_y, des_x, des_y):
    # 把任意一个小块，从src移动到des
    path = get_path(src_x, src_y, des_x, des_y, None, None)
    for i in range(1, len(path)):
        move_space_to(path[i][0], path[i][1], path[i - 1][0], path[i - 1][1])
        swap_neibor(path[i], path[i - 1])


def do_op(op_list):
    # 执行一个操作序列
    space_x, space_y = where_is(xsize - 1, ysize - 1)
    for i in op_list:
        x = space_x - directions[i][0]
        y = space_y - directions[i][1]
        swap_neibor((x, y), (space_x, space_y))
        space_x, space_y = x, y


def get_reverse(a):
    # 求一维序列的逆序数，此处可以进行优化
    ans = 0
    for i in range(len(a)):
        if a[i] != 0:
            for j in range(i + 1, len(a)):
                if a[j] != 0:
                    if a[i] > a[j]:
                        ans ^= 1
    return ans


def is_solvable():
    reverse = get_reverse(a.reshape(-1))
    if ysize % 2 == 0:
        space = where_is(xsize - 1, ysize - 1)
        print(reverse, space, xsize)
        reverse ^= (xsize - 1 - space[0]) & 1
    return reverse == 0


def go():
    if not is_solvable():
        print("unsolvable")
        return
    # 左上部分：xsize-2行，ysize-2列
    for i in range(xsize - 2):
        for j in range(ysize - 2):
            move(*where_is(i, j), i, j)
            ready_flag[i][j] = True
    # 最后两行
    for i in range(ysize - 2):
        move(*where_is(xsize - 1, i), xsize - 1, i)
        if where_is(xsize - 1, ysize - 1) == (xsize - 2, i):
            swap_neibor((xsize - 2, i), (xsize - 2, i + 1))
        if where_is(xsize - 2, i) == (xsize - 2, i): continue
        move(*where_is(xsize - 2, i), xsize - 2, i + 2)
        move_space_to(xsize - 2, i + 1, xsize - 2, i + 2)
        do_op(gold_op)
    # 最后两列，与最后两行对称
    for i in range(xsize - 2):
        move(*where_is(i, ysize - 2), i, ysize - 2)
        if where_is(xsize - 1, ysize - 1) == (i, xsize - 1):
            swap_neibor((i, xsize - 1), (i + 1, xsize - 1))
        if where_is(i, ysize - 1) == (i, ysize - 1): continue
        move(*where_is(i, ysize - 1), i + 2, ysize - 1)
        move_space_to(i + 1, ysize - 1, i + 2, ysize - 1)
        do_op(gold_op_vertical)
    # 最后还有右下角2*2小正方形
    move(*where_is(xsize - 2, ysize - 2), xsize - 2, ysize - 2)
    move(*where_is(xsize - 2, ysize - 1), xsize - 2, ysize - 1)
    move(*where_is(xsize - 1, ysize - 2), xsize - 1, ysize - 2)


def solve(ar):
    global xsize, ysize, a, where, ready_flag, ans_op
    print(ar)
    a = ar
    xsize, ysize = ar.shape
    where = [(-1, -1)] * (xsize * ysize)  # 存储位置信息，便于快速定位
    init_pos()
    ready_flag = [[0] * ysize for _ in range(xsize)]  # 标识此块是否已经拼好，已经拼好就不能再动了
    ans_op = ""
    go()
    print(a)
    print(ans_op)
    return ans_op


if __name__ == '__main__':
    beg_time = time.time()
    solve(problem_generator.random_pintu(xsize, ysize))
    end_time = time.time()
    print('time used', end_time - beg_time)
