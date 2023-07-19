import threading
import time
import math
from typing import List
from Lcode.Lpid import PID
from Lcode.Logger import logger
from Lcode.global_variable import sp_side,lock
put_height=50
fly_height=120
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
            self.x_intergral_base=0
            self.y_intergral_base=0
            self.target=[[0,0],[275,-50],[125,-200],[200,-275],[-25,-350],[275,-350],[50,-275],[50,-125],[200,-125],[125,-50],[-25,-200],[275,-200],[125,-350]]
            self.P1,P2=[0,0],[0,0]
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
                        self.P1=self.target[self.gpio_data[2]]
                        self.P2=self.target[self.gpio_data[3]]-self.target[self.gpio_data[2]]
                        logger.info("进入程控阶段1")
                        pass
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
    
