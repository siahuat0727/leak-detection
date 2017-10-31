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
sp.port = 'COM6'
sp.baudrate = 115200
sp.timeout = 5
sp.open()
plt.ion()
t=0
while t<10000:
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
flag=False
file=open(filename,'w')
for i in y :
    if(flag):
        flag=False
        continue
    if(len(i)==2):
        flag=True
        x=int.from_bytes(i, byteorder='big')
    else :
        x=int.from_bytes(i[0:len(i)-1], byteorder='big')
    z.append(x)
    file.write(str(x))
    file.write("\n")
plt.plot(z)
plt.show()
plt.savefig(picname,dpi=300,format="png")
file.close()
print(len(z)/(tEnd - tStart),"Hz")
print(z[0:1000])
print("end")
