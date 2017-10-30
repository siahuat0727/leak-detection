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
           ## plt.show()
            graph_path = path[:-3] + "png"
            #plt.savefig(graph_path)
            #plt.clf()
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
        data = data - int(np.mean(data))
        seconds = 20
        global peak_num 
        peak_num = 20
        sample_rate = 3918
        time   = np.linspace(0,seconds,data.size)
        new_signal = [0]*3918
        for x in range(0,18):
            W = fftfreq(sample_rate, d = time[1] - time[0])
            f_signal = rfft(data[x*sample_rate:(x+1)*sample_rate])
            ChoosePeak(W,f_signal, new_signal)
        return W, new_signal

def ChoosePeak(W,f_signal, new_signal):
    sorted_signal_index = sorted(range(len(f_signal)), key =  lambda k : f_signal[k])
    sorted_signal = sorted(f_signal)
    sample_rate = 3918
    for x in range(0, peak_num-1):
        new_signal[sorted_signal_index[sample_rate-1-x]] += sorted_signal[sample_rate-1-x]
    return W, f_signal, new_signal

def PlotPeak(location1, location2, file_name):
	path1 , path2 = location1 + file_name, location2 + file_name
	global index
	plt.subplot(6, 3, index)
	title = location1[3:] + file_name[:-4]
	plt.title(title)
	plt.xlim(100, 1000)
	plt.ylim(-10000, 10000)
	W1, new_signal1 = FFT(path1)
	plt.plot(W1,new_signal1, 'g')
	print(title + " is plotted")
	index += 1;
	plt.subplot(6, 3, index)
	title = location2[3:] + file_name[:-4]
	plt.title(title)
	plt.xlim(100, 1000)
	plt.ylim(-10000, 10000)
	W2, new_signal2 = FFT(path2)
	plt.plot(W2,new_signal2, 'g')
	print(title + " is plotted")
	index += 1;
	plt.subplot(6, 3, index)
	title = file_name[:-4] + " leak - no_leak"
	plt.title(title)
	plt.xlim(100, 1000)
	plt.ylim(-10000, 10000)
	plt.plot(W1,np.array(new_signal2) - np.array(new_signal1), 'g')
	print(title + " is plotted")
	index += 1;

def compareTwoFolders(location1, location2, raw=6):
    for x, y in itertools.product(range(1,8), range(0, 100, 20)):
        file_name = get_file_name(x, y)
        path1, path2 = location1 + file_name, location2 + file_name
        if(os.path.exists(path1) and os.path.exists(path2)):
            PlotPeak(location1, location2, file_name)
    plt.show()
index = 1
compareTwoFolders("../4khz_data_no_leak/", "../4khz_data_leak/")


# folders = ["4khz_data_no_leak", "4khz_data_leak"]

# doForAllFolders(folders, plot)
# plot("../no_leak_new/", "open_close.txt")
