import threading
import time
import math
from typing import List
from func.pid import PID
from func.Logger import logger
from func.global_variable import speed_bias,lock,task_start_sign
from external_device.RadarDrivers_reconstruct.Radar import Radar
from external_device.camera_lib.camera import cv_class
from external_device.t265_realsense.t265 import t265_class
put_height=50
fly_height=120
class mission_general(object) :#任务类
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
            self.targetlist=[]
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
                if task_start_sign.value==True :
                    try:
                        if self.mission_step==0:
                            self.mission_step=1
                            self.P1=self.target[self.gpio_data[2]]
                            self.P2=self.target[self.gpio_data[3]]-self.target[self.gpio_data[2]]
                            logger.info("进入程控阶段1")
                            pass
                        else:
                            self.end()
                    except Exception as e:
                        logger.error(e)
                        self.end()
                time.sleep(0.01)
        def gpio_set(self,gpion,value=0):
            self.com_gpio[gpion]=value
        def speed_set(self,x=0,y=0,yaw=0):
            self.com_fc[2]=x+speed_bias
            self.com_fc[3]=y+speed_bias
            self.com_fc[5]=yaw+speed_bias
        def height_set(self,height):
            self.com_fc[4]=height
        def close_height_set(self):
            #发送后屏蔽高度数据源，z方向纯开环速度归零
            self.com_fc[6]=1
        def reopen_height_set(self):
            self.com_fc[6]=0
        def fc_take_off(self):
            self.com_fc[1]=1
        def end(self):
            lock.acquire()
            self.com_fc[1]=0
            #self.com_fc[6]=101
            lock.release()
            logger.info("任务结束")
        def rerun(self):
            #目前没用 
            self.mission_step=0
            self.task_running=True
            logger.info("任务重启")
        def gpio_init(self):
            self.com_gpio[1]=1
            self.com_gpio[2]=64
        def com_init(self):
            self.com_fc[1]=0
            self.com_fc[2]=speed_bias
            self.com_fc[3]=speed_bias
            self.com_fc[4]=fly_height
            self.com_fc[5]=speed_bias
            self.com_fc[6]=0
        def radar_init(self):
            self.radar=Radar()
            self.radar.start('/dev/ttyUSBradar','LD06')
            self.radar.start_resolve_pose(size=1200)
        def t265_init(self):
            self.t265=t265_class()
            self.t265.start_update()
            while self.t265.t265_pose==[0,0,0]:
                #logger.warning("t265未标定完成")
                time.sleep(0.05)
        def camera_init(self):
            self.camera=cv_class()
            self.camera.run()
    
