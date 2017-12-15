import csv
import numpy as np
import scipy.io.wavfile
import matplotlib.pyplot as plt

i = 0
output_file = open("1_20.log","w")


with open('水管1_20.csv') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in spamreader:
        i = i + 1
        if i > 1002:
            arr = ''.join(row)+"\n"
            output_file.write(arr)

wave = np.genfromtxt("1_20.log",dtype = np.int16)
wave = 100 * (wave - int(np.mean(wave)))
plt.plot(wave)
plt.show()
scipy.io.wavfile.write("1_20.wav",40000,wave)
output_file.write(str(i))

output_file.close()

