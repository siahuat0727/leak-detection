import numpy as np
import matplotlib.pyplot as plt
import itertools
import os.path
import scipy.io.wavfile
from scipy.fftpack import rfft, irfft, fftfreq

'''
location  : ../***/***/***/   ex. ../leak/
file_name : ***.*             ex. 1-20.txt
path      : ../***/***/***.*  ex. ../leak/1-20.txt
'''

def toWave(location, file_name, sample_rate=3918):
    path = location + file_name
    if os.path.exists(path):
        with open(path) as f:
            wave = np.genfromtxt(path, dtype = np.int16)
            wave = 300 * (wave - int(np.mean(wave)))
            wave_path = path[:-3] + "wav"
            scipy.io.wavfile.write(wave_path, sample_rate, wave)
            print(wave_path + " is saved")

def plot(location, file_name):
    path = location + file_name
    if os.path.exists(path):
        with open(path) as f:
            data = [int(x) for x in f.readlines()] # if data are separated by '\n'
            # data = [int(x) for x in next(f).split()] # if data are separated by ' '
            # data = data[1000:1500]
            # plt.figure(file_name)
            plt.title(location[3:-1] + "  " + file_name[:-4])
            plt.ylim(280, 420)
            plt.plot(data)
            # plt.show()
            graph_path = path[:-3] + "png"
            # plt.savefig(graph_path)
            # plt.clf()
            print(graph_path + " is plotted")

def get_file_name(x, y, file_type=".txt"):
    return str(x) + "-" + str(y) + file_type

def doForAllFolders(folders, func):
    for location in ["../" + str(x) + "/" for x in folders]:
        for x, y in itertools.product(range(1,8), range(0, 100, 20)):
            file_name = get_file_name(x, y)
            func(location, file_name)

def FFT(path):
    with open(path) as f:
        data = np.genfromtxt(path, dtype = np.int16)
        data = np.asarray(data)
        data = data[:78000]
        data = np.array(data)
        data = data - int(np.mean(data))
        seconds = 20
        time   = np.linspace(0,seconds,data.size)
        W = fftfreq(data.size, d = time[1] - time[0])
        f_signal = rfft(data)
        return W, f_signal

index = 1
def subPlotFFT2(location1, location2, file_name):
	path1 , path2 = location1 + file_name, location2 + file_name
	global index
	plt.subplot(6, 1, index)
	title = file_name[:-4]
	plt.title(title)
# plt.xlim(0, 2000)
	plt.ylim(-50000, 50000)
	W, f_signal = FFT(path1)
	plt.plot(W,f_signal, 'b')
	W, f_signal = FFT(path2)
	plt.plot(W,f_signal, 'r')
	print(title + " is plotted")
	index += 1;

def subPlotFFT(location, file_name):
    path = location + file_name
    W, f_signal = FFT(path)
    global index
    plt.subplot(3, 2, index)
    title = location[3:-1] + " " + file_name[:-4]
    plt.title(title)
    plt.xlim(0, 2000)
    plt.ylim(-50000, 50000)
    plt.plot(W,f_signal)
    print(title + " is plotted")
    index += 1;

def minus(location1, location2, path1, path2, file_name):
    W1, f_signal1 = FFT(path1)
    W2, f_signal2 = FFT(path2)
    global index
    
    plt.subplot(6, 3, index)
    plt.title(file_name)
    plot(location1, file_name) 
    index += 1
    
    plt.subplot(6, 3, index)
    plt.title(file_name)
    plot(location2, file_name) 
    index += 1
    
    plt.subplot(6, 3, index)
#   time = np.linspace(0, 20, 78000)
#   plt.plot(time, r_signal)
#   plt.plot(W1, f_signal1, 'b')
#   plt.plot(W2, f_signal2, 'r')
#   plt.plot(W1, f_signal2 - f_signal1, 'g')
#   index += 1   
    r_signal = irfft(f_signal2 - f_signal1)
    time = np.linspace(0, 20, 78000)
    plt.plot(time, r_signal)
    index += 1
    
    r_signal = 300 * (r_signal - int(np.mean(r_signal)))
    r_signal_path = file_name[:-4] + "-minus.wav"
    r_signal = np.array(np.asarray(r_signal), dtype=np.int16)
    print(type(r_signal[0]))
    scipy.io.wavfile.write(r_signal_path, 3900, r_signal)
    print(r_signal_path + " is saved")

def compareTwoFolders(location1, location2, raw=6):
    for x, y in itertools.product(range(1,5), range(0, 100, 20)):
        file_name = get_file_name(x, y)
        path1, path2 = location1 + file_name, location2 + file_name
        if(os.path.exists(path1) and os.path.exists(path2)):
            minus(location1, location2, path1, path2, file_name)
			# subPlotFFT(location1, file_name)
			# subPlotFFT(location2, file_name)
			# subPlotFFT2(location1, location2, file_name)
    plt.show()

index = 1
compareTwoFolders("../4khz_data_no_leak/", "../4khz_data_leak/")


# folders = ["4khz_data_no_leak", "4khz_data_leak"]

# doForAllFolders(folders, plot)
# plot("../no_leak_new/", "open_close.txt")
