from tkinter import *
from tkinter.font import *

import numpy as np

import pintu_solver
import problem_generator

window = Tk()
window.resizable(False, False)
window.title('pintu solver')
xsize = 5
ysize = 5
width = 600
height = 600
a = problem_generator.random_pintu(xsize, ysize)
ans = pintu_solver.solve(np.copy(a))
ca = Canvas(width=width, height=height, bg='black')
ca.pack()
w = width / ysize
h = height / xsize
for i in range(1, xsize):
    ca.create_line(0, h * i, width, h * i, fill='white')
for i in range(1, ysize):
    ca.create_line(i * w, 0, i * w, height, fill='white')
font = None
for i in range(5, 72):
    font = Font(family="微软雅黑", size=i, weight="bold")
    str_width = font.measure(str((xsize - 1) * ysize + (ysize - 1) + 1))
    str_height = font.metrics('linespace')
    print(str_width, w, h, i)
    if str_width > w * 0.8 or str_height > h * 0.9:
        break
ch = [[None] * ysize for _ in range(xsize)]
space = None
for i in range(xsize):
    for j in range(ysize):
        if a[i][j]:
            ch[i][j] = ca.create_text((j * w + w / 2, i * h + h / 2), text=str(a[i][j]), fill='white', font=font)
        else:
            space = (i, j)
op_index = 0


def go():
    global op_index, space
    o = [(-1, 0), (1, 0), (0, -1), (0, 1)]['上下左右'.index(ans[op_index])]
    x, y = space[0] - o[0], space[1] - o[1]
    ca.coords(ch[x][y], (space[1] * w + w / 2, space[0] * h + h / 2))
    ch[x][y], ch[space[0]][space[1]] = ch[space[0]][space[1]], ch[x][y]
    a[x][y], a[space[0]][space[1]] = a[space[0], space[1]], a[x, y]
    space = x, y
    op_index += 1
    if op_index < len(ans):
        window.after(500, go)


window.after(500, go)
window.mainloop()
