import serial
import numpy as ny
import time
import binascii
import struct
ser0 = serial.Serial('/dev/ttyUSB0', 230400)
if ser0.isOpen == False:
    ser0.open()