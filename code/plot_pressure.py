import numpy as np
import matplotlib.pyplot as plt
import serial
import serial.tools.list_ports
import datetime
import sys
import time
filename=input("filename: ")
picname=input("picturename: ")
filename=filename+".txt"
picname=picname+".png"
y = []
sp = serial.Serial()
sp.port = 'COM8'
sp.baudrate = 9600
sp.timeout = 5
sp.open()
plt.ion()
psi=6894.76
t=0
while t<1000:
    sp.readline()
    t=t+1
tStart = time.time()
t=0
while sp.isOpen():
    text=sp.readline()
    tEnd = time.time()
    y.append(text)
    if (tEnd - tStart)>=20:
        break
z=[]
file=open(filename,'w')
for i in y :
    text=i.decode()
    file.write(text)
    file.write("\n")
    text=text.strip('\r\n')
    z.append((float(text)/psi))
plt.plot(z)
plt.show()
plt.savefig(picname,dpi=300,format="png")
file.close()
print("end")
