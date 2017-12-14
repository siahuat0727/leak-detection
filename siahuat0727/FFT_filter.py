import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import rfft, irfft, fftfreq, fft

time   = np.linspace(0,10,1000)
signal = np.cos(5*np.pi*time) + np.cos(7*np.pi*time)

W = fftfreq(signal.size, d=time[1]-time[0])
f_signal = rfft(signal)
fft_signal = fft(signal)

# If our original signal time was in seconds, this is now in Hz
cut_f_signal = f_signal.copy()
cut_f_signal[(W<6)] = 0

cut_signal = irfft(cut_f_signal)

plt.ion()
for i in range(1):
	plt.clf()
	signal = np.cos(5*np.pi*time + i/10) + np.cos(7*np.pi*time + i/10) * 3
	rfft_signal = rfft(signal)
	fft_signal = np.abs(fft(signal))

	plt.subplot(311)
	plt.plot(time, signal)

	plt.subplot(312)
	plt.xlim(-10, 10)
	plt.ylim(-3000, 3000)
	plt.plot(W, rfft_signal, 'r.')


	plt.subplot(313)
	plt.xlim(-10, 10)
	plt.ylim(-3000, 3000)
	plt.plot(W, fft_signal, 'r.')
	plt.pause(0.03)

'''
fig = plt.figure()
ax1 = fig.add_subplot(311)
ax2 = fig.add_subplot(312)
ax3 = fig.add_subplot(313)
plt.ion()
print("bla")
print("bla")

for i in range (20):
	ax1.clf()
	ax2.clf()
	ax3.clf()
	print(i)
	ax1.plot(time, signal)
	ax2.plot(time, signal)
	ax3.plot(time, signal)
	plt.pause(0.1)
'''
'''
plt.subplot(222)
plt.xlim(-10,10)
plt.plot(W,f_signal)

plt.subplot(223)
plt.xlim(-10,10)
plt.plot(W,fft_signal)

plt.subplot(224)
plt.plot(time,cut_signal)
plt.show()
'''
