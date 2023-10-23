from external_device.t265_realsense.t265 import t265_class
from external_device.RadarDrivers_reconstruct.Radar import Radar
from external_device.camera_lib.camera import cv_class
import time
def t265_test():
    t265=t265_class()
    t265.start_update()
    while True:
        print(t265.t265_pose)
        time.sleep(0.1)
def Radar_test(port,type='LD06',size=1200):
    radar=Radar()
    radar.start(port,type)
    radar.start_resolve_pose(size)
    #time.sleep(1)
    while True:
        print(radar.rt_pose)
        time.sleep(0.1)
