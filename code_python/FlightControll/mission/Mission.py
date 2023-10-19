import threading
import time
import math
from typing import List
from func.pid import PID
from func.Logger import logger
from func.global_variable import sp_side,lock,task_start_sign
from external_device.RadarDrivers_reconstruct.Radar import Radar
from external_device.camera_lib.camera import cv_class
from external_device.t265_realsense.t265 import t265_class
from mission.Mission_general import mission_general
put_height=50
fly_height=120

class mission(mission_general):
    def __init__(self, fc_data, com_fc, com_gpio, gpio_data) -> None:
        super().__init__(fc_data, com_fc, com_gpio, gpio_data)
        self.radar_flag=False
        self.t265_flag=False
        self.cv_flag=False
        if self.radar_flag==True:
            self.radar_init()
        if self.t265_flag==True:
            self.t265_init()
        if self.cv_flag==True:
            self.cv_init()
    def task(self):
        global put_height,fly_height,data_source
        while self.task_running==True :
            if task_start_sign.value==True :
                if self.mission_step==0:
                    self.mission_step=1
                    
                    logger.info("进入程控阶段1")
                    pass
                else:
                    self.end()
            time.sleep(0.01)
