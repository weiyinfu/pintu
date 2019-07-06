# 各种语言的拼图小游戏
## 文件说明
### python
* problem-generator：问题产生器，保证有解
* pintu-solver：拼图求解器
* 拼图界面.py：自动演示怎么玩拼图，基于tkinter

### pintu.html
纯html，js，不依赖第三方库的带AI的拼图游戏

### java
* 基于swing的拼图游戏
* 基于android的拼图游戏

## 算法说明
先还原左上角，再还原最下方两行，再还原最右方两列，最后还原右下角小正方形
