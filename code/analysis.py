import numpy as np
import matplotlib.pyplot as plt
import itertools
import os.path
import scipy.io.wavfile
import wave
import pylab as pl
from scipy.fftpack import rfft, irfft, fftfreq

sample_rate,data = scipy.io.wavfile.read("1-40-minus.wav", mmap=False)
#data = data[3000:]
time   = np.linspace(0,data.size//sample_rate,data.size)
plt.plot(time,data, 'b')
