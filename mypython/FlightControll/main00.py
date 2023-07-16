import os,sys
dir_path = os.path.dirname(os.path.realpath(__file__))
filename = "fc_log.log"
if os.path.isfile(os.path.join(dir_path, filename)):
    os.remove(os.path.join(dir_path, filename))
sys.path.append(os.path.abspath('./yolo_v2'))
#########################################  清除日志  #########################################
from Lcode.global_variable import sp_side,lock
import Lcode.Lserial
import time
from Lcode.Logger import logger
from RadarDrivers_reconstruct.Radar import Radar
import Lcode.Lmission
##############################################变量############################################
rxbuffer=[0,0,3,0,0]#飞控反传标志位 帧头/任务模式（用于确认）/当前任务阶段/阶段切换标志符/帧尾
com_fc = [170, 0, sp_side, sp_side, sp_side, sp_side, 0,sp_side, 255]#发送给飞控的数据 帧头/任务模式/x/y/z/yaw/任务切换标志位/速度偏置量/帧尾
com_gpio =[170,0,0,0,0,0,0,0,0,255]#发送给esp32/arduino的数据 GPIO输出 帧头/GPIO1~8/帧尾
p1,p2=None,None
##########################################  任务  #############################################
""" serial_fc=Lcode.Lserial.Serial_fc("COM4",460800)
serial_fc.port_open()pip
serial_fc.listen_start(rxbuffer)
serial_fc.send_start(com_fc)
serial_gpio=Lcode.Lserial.Serial_gpio("COM5",38400)
serial_gpio.port_open()
serial_gpio.send_start(com_gpio)
#radar=Radar()
#radar.start('COM3','LD06')
mission_task=Lcode.Lmission.mission(rxbuffer,com_fc,com_gpio)
mission_task.run() """
while(1):
    #print(radar.find_obstacles_with_filter())
    print("success")
    time.sleep(0.2)
    pass