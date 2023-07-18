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
                    elif self.mission_step==1:
                        self.x_intergral_base=self.fc_data[1]
                        self.y_intergral_base=self.fc_data[2]
                        x_pid=PID(20,self.P1[0])
                        y_pid=PID(20,self.P1[1])
                        self.mission_step=2
                        logger.info("阶段2,前往P1")
                    elif self.mission_step==2:
                        if math.abs(x_pid.get(self.fc_data[1]-self.x_intergral_base))>3 or math.abs(y_pid.get_pid(self.fc_data[2]-self.y_intergral_base))>3:
                            self.speed_set(x_pid.get(self.fc_data[1]-self.x_intergral_base),y_pid.get_pid(self.fc_data[2]-self.y_intergral_base),fly_height,0)
                            self.change_count=0
                        else:
                            self.change_count+=1
                        if self.change_count>5:
                            self.mission_step=3
                            self.change_count=0
                            self.time_count=time.time()
                            logger.info("阶段3,悬停5s 放货")
                    elif self.mission_step==3:
                        if time.time()-self.time_count<5:
                            self.speed_set(x_pid.get(self.fc_data[1]-self.x_intergral_base),y_pid.get_pid(self.fc_data[2]-self.y_intergral_base),put_height,0)
                            self.change_count=0
                        else:
                            self.change_count+=1
                        if self.change_count>5:
                            self.mission_step=4
                            self.change_count=0
                            self.time_count=time.time()
                            logger.info("阶段4,悬停3s等待回复高度")
                    elif self.mission_step==4:
                        if time.time()-self.time_count<5:
                            self.speed_set(x_pid.get(self.fc_data[1]-self.x_intergral_base),y_pid.get_pid(self.fc_data[2]-self.y_intergral_base),fly_height,0)
                            self.change_count=0
                        else:
                            self.change_count+=1
                        if self.change_count>5:
                            self.mission_step=5
                            self.change_count=0
                            self.x_intergral_base=self.fc_data[1]
                            self.y_intergral_base=self.fc_data[2]
                            x_pid=PID(20,self.P2[0])
                            y_pid=PID(20,self.P2[1])
                            logger.info("阶段5,前往P2")
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
    
