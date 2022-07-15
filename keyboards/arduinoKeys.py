import serial
import time

# Constants
arduino = serial.Serial(port='COM5', baudrate=250000)
time.sleep(2)

def press(key, n, down_time=0.05, up_time=0.1):
    for _ in range(n):
        arduino.write(bytes(f'press;{key};{down_time*1000};{up_time*1000};', 'utf-8')) # *1000 to synchronize with time.sleep func in python

def key_down(key):
    arduino.write(bytes(f'pressDown;{key};0;0;', 'utf-8'))

def key_up(key):
    arduino.write(bytes(f'pressUp;{key};0;0;', 'utf-8'))

def releaseAll():
    arduino.write(bytes(f'releaseAll;', 'utf-8'))