import threading
from multiprocessing import Value
speed_bias=51 #串口传输速度偏置量
lock=threading.Lock()#线程锁
task_start_sign=Value("b",False)#飞控阶段标志位 当进入程序控制阶段时变为True