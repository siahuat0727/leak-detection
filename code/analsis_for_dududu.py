import numpy as np
import matplotlib.pyplot as plt
import itertools
import os.path
import scipy.io.wavfile
import wave
import pylab as pl
from scipy.fftpack import rfft, irfft, fftfreq
from scipy import stats

sample_rate,data = scipy.io.wavfile.read("dududu.wav", mmap=False)
time   = np.linspace(0,data.size//sample_rate,data.size)
w = fftfreq(data.size,d = time[1] - time[0])
f_data = rfft(data)
a = np.array(f_data)
a = a[a >= 0]
a = np.round(a)

#print("sample rate:",sample_rate)
print(stats.mode(a))
print(stats.tmax(a))      

#plt.ylim(-1000000,2000000)
plt.plot(w,f_data)
plt.show()
