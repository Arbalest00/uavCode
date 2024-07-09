import serial
ser0 = serial.Serial('COM10', 115200)#发
ser1 = serial.Serial('COM3', 115200)#收
if ser1.isOpen  ==False:
    ser1.open()
if ser0.isOpen  ==False:
    ser0.open()
rxbuffer = []
while  True:
    size = ser1.inWaiting()
    if size !=0:
        try:
            response = ser1.read(1)
            #print(response)
            if response==b'\xAA':
                ser0.write(response)
                response = ser1.read(1)
                #print(response)
                while response!=b'\xFF':
                    rxbuffer.append(response)
                    ser0.write(response)
                    response = ser1.read(1)
                ser0.write(response)
            else:
                continue
            
            rxbuffer.clear()
        except:
            continue