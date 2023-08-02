import socket
import time

#client 发送端
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
PORT = 2887
mslist=[170,2,4,255]
while True:
      start = time.time()  #获取当前时间
      print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(start)))  #以指定格式显示当前时间
      server_address = ("192.168.137.136", PORT)  # 接收方 服务器的ip地址和端口号
      for value in mslist:
            hex_value = hex(value)[2:].zfill(2).encode('utf-8')  # 将数组中的每个值转换成16进制字符串
            client_socket.sendto(hex_value, server_address) #将msg内容发送给指定接收方
            print("发送的内容是:",hex_value)  #打印发送的内容
      time.sleep(0.05)