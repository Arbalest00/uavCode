import cv2
from Lcode.Logger import logger
import threading
from RadarDrivers_reconstruct.Radar import Radar
from Lcode.global_variable import lock
import time
class cv_cap(object):
    def __init__(self,width,height) -> None:
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        self.cap_running=False
    def run(self,img):
        self.cap_running=True
        cap_thread=threading.Thread(target=self.cap_thread,args=(img,))
        cap_thread.daemon=True
        cap_thread.start()
        logger.info("摄像头启动")
    def cap_thread(self,img):
        while self.cap_running==True:
            img=self.cap.read()[1]
            if img is None:
                logger.error("摄像头读取失败")
                continue
            time.sleep(0.01)
    def stop(self):
        self.cap_running=False
        logger.info("摄像头关闭")
""" class radar_cap(object):
    def __init__(self,port='COM3',name='LD06') -> None:
        self.radar=Radar()
        self.radar.start(port,name)
        self.radar_running=False
    def run(self,point1=None,point2=None):
        self.radar_running=True
        radar_thread=threading.Thread(target=self.radar_thread,args=(point1,point2))
        radar_thread.daemon=True
        radar_thread.start()
        logger.info("雷达启动")
    def radar_thread(self,point1=None,point2=None):
        while self.radar_running==True:
            lock.acquire()
            point1,point2=self.radar.find_obstacles_with_filter()
            lock.release
            time.sleep(0.02)
    def stop(self):
        self.radar_running=False
        logger.info("雷达关闭") """