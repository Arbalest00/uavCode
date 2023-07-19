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
##############################################变量############################################
rxbuffer_fc=[0,0,0]#飞控反传信息 任务模式/x积分值/y积分值
rxbuffer_gpio=[0,0,0,0]#gpio反传信息,启动/模式/P1/P2
com_fc = [170, 0, sp_side, sp_side, 120, sp_side, 0,sp_side, 255]#发送给飞控的数据 帧头/任务模式/x/y/z高度/yaw/任务切换标志位/速度偏置量/帧尾
com_gpio =[170,0,0,0,0,0,0,0,0,0,0,255]#发送给esp32/arduino的数据 GPIO输出 帧头/GPIO1~10/帧尾
run_sign=False
##########################################  任务  #############################################
""" serial_fc=Lcode.Lserial.Serial_fc("COM4",460800)
serial_fc.port_open()
serial_fc.listen_start(rxbuffer)
serial_fc.send_start(com_fc) """
serial_gpio=Lcode.Lserial.Serial_gpio("COM5",38400)
serial_gpio.port_open()
serial_gpio.send_start(com_gpio)
serial_gpio.listen_start(rxbuffer_gpio)
#radar=Radar()
#radar.start('COM3','LD06')

while(1):
    """ if run_sign==False:
        if rxbuffer_gpio[1]==1:
            run_sign=True
            if rxbuffer_gpio[0]==1:
                from Lcode.Lmission.Lmission_okr01 import mission
                mission_task=mission(rxbuffer_fc,com_fc,com_gpio,rxbuffer_gpio)
                mission_task.run()
            elif rxbuffer_gpio[0]==2:
                from Lcode.Lmission.Lmission_okr02 import mission
                mission_task=mission(rxbuffer_fc,com_fc,com_gpio,rxbuffer_gpio)
                mission_task.run()
            elif rxbuffer_gpio[0]==3:
                from Lcode.Lmission.Lmission_okr03 import mission
                mission_task=mission(rxbuffer_fc,com_fc,com_gpio,rxbuffer_gpio)
                mission_task.run() """
    time.sleep(0.2)
    pass