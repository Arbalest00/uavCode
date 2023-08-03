import os,sys
dir_path = os.path.dirname(os.path.realpath(__file__))
filename = "fc_log.log"
if os.path.isfile(os.path.join(dir_path, filename)):
    os.remove(os.path.join(dir_path, filename))
sys.path.append(os.path.abspath('./yolo_v2'))
os.system("netsh wlan connect name= LESP32WF")
#########################################  清除日志  #########################################
from Lcode.global_variable import sp_side,lock
import Lcode.Lprotocol
import time
from Lcode.Logger import logger
from RadarDrivers_reconstruct.Radar import Radar
from Lcode.Lmission.Lmission_final import mission
##############################################变量############################################
rxbuffer_fc=[0,0,0]#飞控反传信息 任务模式/x积分值/y积分值
rxbuffer_gpio=[0,0,0,0]#gpio反传信息,启动/P1/P2/模式
com_fc = [170, 0, sp_side, sp_side, 120, sp_side, 0,sp_side, 255]#发送给飞控的数据 帧头/启动命令/x/y/z高度/yaw/任务切换标志位/速度偏置量/帧尾
com_gpio =[170,0,0,0,0,1,1,1,1,255]#发送给esp32/arduino的数据 GPIO输出 帧头/低功率输出/高功率输出
run_sign=False
##########################################  任务  #############################################
""" serial_fc=Lcode.Lprotocol.Serial_fc("COM4",460800)
serial_fc.port_open()
serial_fc.listen_start(rxbuffer_fc)
serial_fc.send_start(com_fc) """
""" serial_gpio=Lcode.Lprotocol.Serial_gpio("COM5",38400)
serial_gpio.port_open()
serial_gpio.send_start(com_gpio) """
#serial_gpio.listen_start(rxbuffer_gpio)
mission=mission(rxbuffer_fc,com_fc,com_gpio,rxbuffer_gpio)
mission.run() 
""" radar=Radar()
radar.start('COM3','LD06')
radar.start_resolve_pose() """
while(1):
    #print(radar.rt_pose)
    time.sleep(0.5)