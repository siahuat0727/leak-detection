import numpy as np
import matplotlib.pyplot as plt
import serial
import serial.tools.list_ports
import datetime
import sys
#coms=serial.tools.list_ports.comports()
filename=input("filename: ")
picname=input("picturename: ")
filename=filename+".txt"
picname=picname+".png"
plt.ion()  
y = []
"""for a in coms:
     print (a)
"""
sp = serial.Serial()
sp.port = 'COM7'
sp.baudrate = 9600
sp.timeout = 5
sp.open()
start = datetime.datetime.now()
end=start
sp.readline()
file=open(filename,'w')
while sp.isOpen():
    text=sp.readline().decode()
    file.write(text)
    text=text.strip('\r\n')
    y.append(int(text))
    end=datetime.datetime.now()
    time=end-start
    if (time.seconds)>=40:
        break
plt.plot(y)
plt.savefig(picname,dpi=300,format="png")
plt.show()
file.close()
print("end")

