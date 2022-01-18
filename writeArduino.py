import serial
import time


ser = serial.Serial('COM5', 9600, timeout=1)
time.sleep(2)
input()
ser.write(bytes([1]))
input()
ser.write(bytes([2]))