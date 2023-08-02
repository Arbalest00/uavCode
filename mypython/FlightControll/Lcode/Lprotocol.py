import serial
import threading
import socket
from typing import List
from Lcode.Logger import logger
import time
from Lcode.global_variable import lock,task_start_sign
DEBUG=False
class Serial_fc(object):
    def __init__(self,port,baudrate):
        self.ser=serial.Serial(port=port,baudrate=baudrate)
        self.fclisten_running=False
        self.fcsend_running=False
        self.rate=460800
        self.startbyte=b'\xAA'
        self.endbyte=0xFF
    def port_open(self):
        self.ser.close()
        if self.ser.is_open==False:
            self.ser.open()
            logger.info("目前飞控串口状态：%s",self.ser.is_open)
    def listen_start(self,rxbuffer:List[int]):
        self.fclisten_running=True
        listen_thread=threading.Thread(target=Serial_fc.listen_fc,args=(self,rxbuffer))
        listen_thread.daemon=True
        listen_thread.start()
        logger.info("飞控串口监听线程启动")
    def listen_end(self):
        self.fclisten_running=False
        logger.info("飞控串口监听线程关闭")
    def listen_fc(self,rxbuffer:List[int]):
        while self.fclisten_running ==True:
            byte_data = self.ser.read() 
            if byte_data == self.startbyte:
                # 读取接下来的四个字节数据
                recv = self.ser.read(6)
                # 判断数据是否符合通信协议，即以0xFF结尾
                if recv[5] == self.endbyte:
                    intergral_x = ((recv[1] << 8) | recv[2])-0x4000
                    intergral_y = ((recv[3] << 8) | recv[4])-0x4000
                    rxbuffer.clear()
                    rxbuffer.append(recv[0])
                    rxbuffer.append(intergral_x)
                    rxbuffer.append(intergral_y)
                    if recv[0]==0x05:
                        task_start_sign.value=True
                    else:
                        task_start_sign.value=False
                    if DEBUG :
                        logger.info(rxbuffer)
            time.sleep(0.05)
    def send_fc(self,comlist:List[int]):
        while self.fcsend_running==True:
            for value in comlist:
                hex_value = hex(value)[2:].zfill(2)  # 将数组中的每个值转换成16进制字符串
                self.ser.write(bytes.fromhex(hex_value))  # 将16进制字符串转换为字节并发送到串口
            time.sleep(0.01)
    def send_start(self,comlist:List[int]):
        self.fcsend_running=True
        fcsend_thread=threading.Thread(target=Serial_fc.send_fc,args=(self,comlist))
        fcsend_thread.daemon=True
        fcsend_thread.start()
        logger.info("飞控串口发送线程启动")
    def send_end(self):
        self.fcsend_running=False
        logger.info("飞控串口发送线程关闭")
        
class Serial_gpio(object):
    def __init__(self,port,baudrate):
        self.ser=serial.Serial(port=port,baudrate=baudrate)
        self.gpiosend_running=False
        self.gpiolisten_running=False
        self.rate=460800
    def port_open(self):
        self.ser.close()
        if self.ser.is_open==False:
            self.ser.open()
            logger.info("目前gpio串口状态：%s",self.ser.is_open)
    def send_gpio(self,comlist:List[int]):
        while self.gpiosend_running==True:
            for value in comlist:
                hex_value = hex(value)[2:].zfill(2)  # 将数组中的每个值转换成16进制字符串
                self.ser.write(bytes.fromhex(hex_value))  # 将16进制字符串转换为字节并发送到串口
            time.sleep(0.02)
    def send_start(self,comlist:List[int]):
        self.gpiosend_running=True
        gpiosend_thread=threading.Thread(target=Serial_gpio.send_gpio,args=(self,comlist))
        gpiosend_thread.daemon=True
        gpiosend_thread.start()
        logger.info("gpio串口发送线程启动")
    def send_end(self):
        self.gpiosend_running=False
        logger.info("gpio串口发送线程关闭")
    def listen_start(self,rxbuffer:List[int]):
        self.gpiolisten_running=True
        listen_thread=threading.Thread(target=Serial_gpio.listen_gpio,args=(self,rxbuffer))
        listen_thread.daemon=True
        listen_thread.start()
        logger.info("gpio串口监听线程启动")
    def listen_end(self):
        self.gpiolisten_running=False
        logger.info("gpio串口监听线程关闭")
    def listen_gpio(self,rxbuffer:List[int]):
        while self.gpiolisten_running ==True:
            byte_data = self.ser.read() 
            if byte_data == b'\xAA':
                # 读取接下来的四个字节数据
                recv = self.ser.read(5)
                # 判断数据是否符合通信协议，即以0xFF结尾
                if recv[4] == 0xFF:
                    lock.acquire()
                    rxbuffer.clear()
                    for i in range(0,4):
                        rxbuffer.append(recv[i])
                    if task_start_sign.value ==False:
                        logger.info(rxbuffer)
                    lock.release()
            time.sleep(0.05)
class udp_terminal(object):
    def __init__(self,ip='0.0.0.0',port=2887):
        self.udp_socket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.bind((ip,port))
        self.udp_listen_running=False
        self.task_list=[]
        self.takeoff_sign=False
        self.fall_sign=False
        self.food_all_take=False
    def listen_start(self):
        self.udp_listen_running=True
        listen_thread=threading.Thread(target=udp_terminal.listen_udp,args=(self,))
        listen_thread.daemon=True
        listen_thread.start()
        logger.info("udp监听线程启动")
    def listen_end(self):
        self.udp_listen_running=False
        logger.info("udp监听线程关闭")
    def listen_udp(self):
        received_data=[]
        state=0
        while self.udp_listen_running==True:
            data, client_address = self.udp_socket.recvfrom(1024)
            #logger.info("接收到的数据是%s",data)
            if state==0 and data==b'\xaa':
                received_data.clear()
                state=1
                #print('1')
            elif state==1 and len(received_data)<2:
                received_data.append(int(data.decode()))
                #print('2')
            elif len(received_data)==2 and data==b'\xff':
                #print('3')
                if received_data[0]!=0xA0:
                    received_data.append(0)
                    self.task_list.append(received_data[:])
                    self.food_all_take=False
                    self.tasksort()
                    logger.info("点和优先级是:%s",received_data)
                    logger.info("任务列表是:%s",self.task_list)
                    logger.info("新任务下达，返回出发点")
                elif received_data[0]==0xA0:
                    if received_data[1]==0xA0:
                        self.fall_sign=True
                        logger.info("降落取餐")
                    elif received_data[1]==0xA1:
                        self.takeoff_sign=True
                        logger.info("起飞前往下一点")
                else:
                    pass
                state=0
            time.sleep(0.02)
    def tasksort(self):
        self.task_list.sort(key=lambda x:x[0],reverse=True)
        logger.info("任务列表排序后:%s",self.task_list)