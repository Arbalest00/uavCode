import threading
import time
import math
from typing import List
from Lcode.Lpid import PID
from Lcode.Logger import logger
from Lcode.global_variable import sp_side,lock
from RadarDrivers_reconstruct.Radar import Radar
put_height=50
fly_height=120
threshold=5
radar=Radar()
radar.start('COM3','LD06')
class mission(object) :
        #左正右负，前正后负
        def __init__(self,fc_data:List[int],com_fc:List[int],com_gpio:List[int],gpio_data:List[int]) -> None:
            self.fc_data=fc_data
            self.com_fc=com_fc
            self.com_gpio=com_gpio
            self.gpio_data=gpio_data
            self.mission_step=0
            self.task_running=False
            self.time_count=0
            self.change_count=0
            self.bias=[0,0]
            self.self_pos = [0,0]
            self.target = [[130,491],[407.440],[252,288],[325,213],[99,139],[402,138],[174,213],[175,364],[328,365],[252,440],[100,288],[404,287],[248,139]]
            self.P1=[0,0]
            self.P2=[0,0]
        def run(self):
            self.task_running=True
            task_thread=threading.Thread(target=self.task)
            task_thread.daemon=True
            task_thread.start()
            self.mission_step=0
            logger.info("任务启动")
            pass
        def task(self):
            global put_height,fly_height
            while self.task_running==True :
                self.fc_mission_step = self.fc_data[0]
                if self.fc_mission_step ==0x05 :
                    if self.mission_step==0:
                        self.mission_step=1
                        """ self.bias=[int(radar.rt_pose[0])-self.target[0][0],int(radar.rt_pose[1])-self.target[0][1]]
                        for i in range(len(self.target)):
                            self.target[i][0] += self.bias[0]
                            self.target[i][1] += self.bias[1] """
                        self.P1=self.target[self.gpio_data[2]]
                        self.P2=self.target[self.gpio_data[3]]
                        logger.info("取得偏置，设置点位，准备开始")
                        x_pid = PID(20,self.P1[0])
                        y_pid = PID(20,self.P1[1])
                    elif self.mission_step==1:
                        if abs((int(radar.rt_pose[0])-self.P1[0]))>threshold or abs((int(radar.rt_pose[1])-self.P1[1]))>threshold:
                            self.speed_set(x_pid(int(radar.rt_pose[0])),y_pid(int(radar.rt_pose[1])))
                            self.height_set(fly_height)
                        else:
                            self.mission_step=2
                            self.time_count=time.time()
                            logger.info("到达P1，悬停开始")
                    elif self.mission_step==2:
                        if time.time()-self.time_count<5:
                            self.speed_set(x_pid(int(radar.rt_pose[0])),y_pid(int(radar.rt_pose[1])))
                            self.height_set(put_height)
                        else:
                            self.mission_step=3
                            self.time_count=time.time()
                            logger.info("悬停结束，恢复高度")
                    elif self.mission_step==3:
                        if time.time()-self.time_count<5:
                            self.speed_set(x_pid(int(radar.rt_pose[0])),y_pid(int(radar.rt_pose[1])))
                            self.height_set(fly_height)
                        else:
                            self.mission_step=4
                            logger.info("测试结束 准备降落")
                    else:
                        self.end()
            time.sleep(0.01)
        def gpio_set(self,gpion,value=0):
            self.com_gpio[gpion]=value
        def speed_set(self,x=0,y=0,yaw=0):
            self.com_fc[2]=x+sp_side
            self.com_fc[3]=y+sp_side
            self.com_fc[5]=yaw+sp_side
        def height_set(self,height):
            self.com_fc[4]=height
        def end(self):
            lock.acquire()
            self.com_fc[6]=1
            lock.release()
            logger.info("任务结束")
    
