import socket
import time

port = 2887
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
address = ("0.0.0.0", port)
server_socket.bind(address)
print("接收启动")

read_started = False
received_data = []
state=0
while True:
    data, client_address = server_socket.recvfrom(1024)
    print("接收到的数据是",data)
    if state==0 and data==b'\xaa':
        state=1
        #print('1')
    elif state==1 and len(received_data)<2:
        received_data.append(int(data.decode()))
        #print('2')
    elif len(received_data)==2 and data==b'\xff':
        #print('3')
        state=0
        print("点和优先级是:",received_data)
        received_data.clear()
    time.sleep(0.02)
