import threading
import time
import math
from typing import List
from Lcode.Lpid import PID
from Lcode.Logger import logger
from Lcode.global_variable import sp_side,lock,task_start_sign
from Lcode.Lprotocol import udp_terminal
from RadarDrivers_reconstruct.Radar import Radar
from t265_realsense import t265
put_height=50
fly_height=150
#realsense=t265.t265_class()
threshold=5
udp=udp_terminal()
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
            self.t265sign=False
            self.x_intergral_base=0
            self.y_intergral_base=0
            self.pointcount=0
            self.iscvcap=False
            self.xyz=[0,0,0]
            self.xy=[170,int(self.xyz[0]),int(self.xyz[1]),255]
            self.yaw=0
            self.target=[[0,-400],[320,-400],[320,0],[80,0],[80,-320],[240,-320],[240,-80],[160,-80],[160,-240],[0,0]]
        def run(self):
            self.task_running=True
            #realsense.autoset()
            udp.send_start("192.168.4.255",2887,self.xy)
            self.t265sign=True
            task_thread=threading.Thread(target=self.task)
            task_thread.daemon=True
            task_thread.start()
            self.mission_step=0
            logger.info("任务启动 t265标定")
            pass
        def task(self):
            global put_height,fly_height
            while self.task_running==True :
                """ if self.t265sign==True:
                        self.xyz=realsense.get_actual_pos()
                        self.yaw=realsense.get_actual_yaw()
                        logger.info("t265返回数据为%s",self.xyz) """
                if task_start_sign.value==True :
                    if self.mission_step==0:
                        logger.info("开始延时")
                        self.time_count=time.time()
                        self.mission_step=1
                    elif self.mission_step==1:
                        if time.time()-self.time_count<3:
                            pass
                        else:
                            logger.info("前进")
                            self.mission_step=2
                    elif self.mission_step==2:
                        if self.pointcount<len(self.target) and self.iscvcap==False:
                            self.move_point(self.target[self.pointcount])
                        elif self.iscvcap==True:
                            self.mission_step=2
                            self.iscvcap=False
                            logger.info("发现火源 开始接近")
                        else:
                            logger.info("gg")
                            self.mission_step=101
                    elif self.mission_step==2: #发现火源后处理阶段 处理完成后返回阶段1
                        self.mission_step=101
                        pass
                    else:
                        self.end()
                time.sleep(0.05)
        def fc_take_off(self):
            self.com_fc[1]=1
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
            self.com_fc[6]=101
            lock.release()
            logger.info("任务结束")
        def rerun(self):
            self.mission_step=0
            self.task_running=True
            logger.info("任务重启")
            pass
        def gpio_init(self):
            self.com_gpio[1]=1
            self.com_gpio[2]=64
        def com_init(self):
            self.com_fc[1]=0
            self.com_fc[2]=sp_side
            self.com_fc[3]=sp_side
            self.com_fc[4]=fly_height
            self.com_fc[5]=sp_side
            self.com_fc[6]=0
        def move_point(self,point):
            x_pid=PID(0,point[0])
            y_pid=PID(0,point[1])
            yaw_pid=PID(1,0)
            while(abs(self.xyz[0]-point[0])>threshold or abs(self.xyz[1]-point[1])>threshold) and self.iscvcap==False:
                self.xyz=realsense.get_actual_pos()
                self.yaw=realsense.get_actual_yaw()
                x_speed=x_pid.get_pid(self.xyz[0])
                y_speed=y_pid.get_pid(self.xyz[1])
                yaw_speed=yaw_pid.get_pid(self.yaw)
                logger.info("x=%d,y=%d",self.xyz[0]-point[0],self.xyz[1]-point[1])
                logger.info("xs=%d,ys=%d,yaws=%d",x_speed,y_speed,yaw_speed)
                self.speed_set(x_speed,y_speed,-yaw_speed)
            if self.iscvcap==False:
                self.pointcount+=1
