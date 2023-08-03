import socket
import time
import pickle
import numpy as np
import cv2
from Lgui import tk_gui, cv_draw 
import tkinter as tk
port = 2887
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
recv_address = ("0.0.0.0", port)
send_address = ("255.255.255.255", port)
server_socket.bind(recv_address)
server_socket.settimeout(0.1)
print("接收启动")
received_data = []
datalist=[[0,0]]
timecount=0
lastxy=[0,0]
lastdata=[0,0]
def main():
    global datalist,img,timecount,received_data,gui,lastxy,lastdata
    try:
        data, client_address = server_socket.recvfrom(1024)
        #print("接收到的数据是",data)
        realdata=pickle.loads(data)
        if realdata[0]==170 and realdata[3]==255:
            received_data=[realdata[1],realdata[2]]
            datalist.append(received_data)
            lastdata=received_data
            print("realdata x y",received_data)
            realdata.clear()
    except:
        pass 
    if gui.task_id==1:
        senddata=[170,160,160,255]
        bydata=pickle.dumps(senddata)
        send_socket.sendto(bydata, send_address)
    elif gui.task_id==2:
        senddata=[170,160,161,255]
        bydata=pickle.dumps(senddata)
        send_socket.sendto(bydata, send_address)
    if gui.ready_to_go==True:
        senddata=[170,192,192,255]
        bydata=pickle.dumps(senddata)
        send_socket.sendto(bydata, send_address)
    if time.time()-timecount>1:
        distance=int(((lastdata[0]-lastxy[0])**2+(lastdata[1]-lastxy[1])**2)**0.5)
        #text="distance:{}".format(str(distance))
        gui.output_text2.configure(text="distance: {}".format(distance))
        img=draw.show_draw_res(datalist)
        timecount=time.time()
        gui.show_img(img)
    gui.root.after(50,main)
draw=cv_draw()
gui=tk_gui()
gui.output_text2=tk.Label(gui.root, text="", font=gui.label_font, anchor=tk.CENTER)
gui.output_text2.pack(padx=10, pady=10, side=tk.BOTTOM)
gui.root.after(100,main)
gui.gui_window()
gui.root.mainloop()
