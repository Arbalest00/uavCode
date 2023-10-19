import serial
import threading
import pickle
import socket
from typing import List
from func.Logger import logger
import time
from func.global_variable import lock,task_start_sign
DEBUG=False
class udp_terminal(object):
    def __init__(self):
        self.udp_socket=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_listen_running=False
        self.udp_send_running=False
        self.takeoff_sign=False
        self.task_hjm=False
        self.task_number=0
    def listen_start(self,IP,PORT):
        self.udp_listen_running=True
        self.udp_socket.bind((IP,PORT))
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
            realdata=pickle.loads(data)
            if realdata[0]==170 and realdata[3]==255:
                if realdata[1]==160 and realdata[2]==160:
                    self.task_number=1
                elif realdata[1]==160 and realdata[2]==161:
                    self.task_number=2
                elif realdata[1]==192 and realdata[2]==192:
                    self.task_hjm=True
            time.sleep(0.02)
    """ def tasksort(self):
        self.task_list.sort(key=lambda x:x[0],reverse=True)
        logger.info("任务列表排序后:%s",self.task_list) """
    
    def send_start(self,IP,PORT,senddata):
        self.udp_send_running=True
        self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # 设置允许发送广播数据
        send_thread=threading.Thread(target=udp_terminal.send_udp,args=(self,IP,PORT,senddata))
        send_thread.daemon=True
        send_thread.start()
        logger.info("udp发送线程启动")
    def send_udp(self,IP,PORT,senddata):
        while self.udp_send_running==True:
            changedata=pickle.dumps(senddata)
            self.udp_socket.sendto(changedata,(IP,PORT))
            time.sleep(0.05)