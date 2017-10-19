import pyfirmata
import numpy as np
import matplotlib.pyplot as plt
import serial
import serial.tools.list_ports
import datetime
import sys
import time
from time import sleep
from pyfirmata import Arduino, util
y=[]
t=0
plt.ion()  
PORT="COM8"
board=pyfirmata.Arduino(PORT)
tStart = time.time()
board.analog[0].enable_reporting()
it = util.Iterator(board)
it.start()
while True:
    read=board.analog[0].read()
    sleep(0.000001)   
    if(read==None):
        continue
    y.append(read)
    tEnd = time.time()
    if (tEnd - tStart)>=10:
        break
    
print(y[0:500])
plt.plot(y)
print(len(y)/(tEnd - tStart),"Hz")
