import os,sys
dir_path = os.path.dirname(os.path.realpath(__file__))
filename = "fc_log.log"
if os.path.isfile(os.path.join(dir_path, filename)):
    os.remove(os.path.join(dir_path, filename))
#os.system("netsh wlan connect name= LESP32WF")
#########################################  清除日志  #########################################
from func.global_variable import speed_bias,lock
from communication.serial_protocol import Serial_fc,Serial_gpio
import time
from func.Logger import logger
from mission.Mission import mission
import module_test
##############################################变量############################################
# rxbuffer_fc=[0,0,0]#飞控反传信息 任务模式/x积分值/y积分值
# rxbuffer_gpio=[0,0,0,0]#gpio反传信息,启动/P1/P2/模式
# com_fc = [170, 0, speed_bias, speed_bias, 120, speed_bias, 0,speed_bias, 255]#发送给飞控的数据 帧头/启动命令/x/y/z高度/yaw/任务切换标志位/速度偏置量/帧尾
# com_gpio =[170,0,0,0,0,0,0,0,0,255]#发送给esp32/arduino的数据 GPIO输出 帧头/低功率输出/高功率输出
""" run_sign=False
recv_address='0.0.0.0'
recv_port=3333 """
##########################################  任务  #############################################
# serial_fc=Serial_fc("/dev/ttyAMA0",460800)
# serial_fc.port_open()
# serial_fc.listen_start(rxbuffer_fc)
# serial_fc.send_start(com_fc)
""" serial_gpio=Serial_gpio("/dev/ttyUSBArduino",38400)
serial_gpio.port_open()
serial_gpio.send_start(com_gpio)
serial_gpio.listen_start(rxbuffer_gpio) """
""" terminal=communication.udp_protocol.udp_terminal()
terminal.listen_start(recv_address,recv_port) """
#mission=mission(rxbuffer_fc,com_fc,com_gpio,rxbuffer_gpio)
#mission.run()
module_test.t265_test()
#module_test.Radar_test('/dev/ttyUSB0')
while(1):
    time.sleep(0.1)