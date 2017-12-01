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

def readToList(path, spread='\n'):
    if os.path.exists(path):
        with open(path) as f:
            f.readline()
	    f.readline()
	    if spread == '\n':
		data = [int(x) for x in f.readlines()] # if data are separated by '\n'
	    elif spread == ' ':
		data = [int(x) for x in next(f).split()] # if data are separated by ' '
	    return data

def txtToWav(location, file_name, sample_rate=40000):
    path = location + file_name
    if os.path.exists(path):
        with open(path) as f:
            wave = np.genfromtxt(path, dtype = np.int16)
            wave = np.asarray(wave)
            wave = wave[3000:]
            wave = np.array(wave)
            print("mean =", np.mean(wave))
            wave = 50 * (wave - int(np.mean(wave)))
            print("max =", np.max(wave))
            print("min =", np.min(wave))
            wave_path = path[:-3] + "wav"
            scipy.io.wavfile.write(wave_path, sample_rate, wave)
            print(wave_path + " is saved")
    else:
        print(path, "DNE")

def txtToGraph(location, file_name, save=False):
    path = location + file_name
    if os.path.exists(path):
        with open(path) as f:
            f.readline()
            f.readline()
            data = [int(x) for x in f.readlines()] # if data are separated by '\n'
            # data = [int(x) for x in next(f).split()] # if data are separated by ' '
            # data = data[1000:1500]
            # plt.figure(file_name)
            plt.title(location[3:-1] + "  " + file_name[:-4])
            graph_path = path[:-3] + "png"
            if save == False:
                plt.plot(data)
                plt.show()
            else:
                plt.savefig(graph_path)
                plt.clf()
            print(graph_path + " is plotted")
    else:
        print(path, "DNE")

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
        data = data[3000:350000]
        data = np.array(data)
        data = data - int(np.mean(data))
        sample_rate = 40000
        time   = np.linspace(0,data.size//sample_rate,data.size)
        W = fftfreq(data.size, d = time[1] - time[0])
        f_signal = rfft(data)
        return W, f_signal

index = 1
# plot 2 file together
def subPlotFFT2(location1, location2, file_name):
    path1 , path2 = location1 + file_name, location2 + file_name
    global index
    plt.subplot(6, 1, index)
    title = file_name[:-4]
    plt.title(title)
    plt.xlim(100, 800)
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

def compareTwoFolders(location1, location2, raw=6):
    for x, y in itertools.product(range(1,5), range(0, 100, 20)):
        file_name = get_file_name(x, y)
        path1, path2 = location1 + file_name, location2 + file_name
        if(os.path.exists(path1) and os.path.exists(path2)):
            # subPlotFFT(location1, file_name)
            # subPlotFFT(location2, file_name)
            # subPlotFFT2(location1, location2, file_name)
    plt.show()

# compareTwoFolders("../4khz_data_no_leak/", "../4khz_data_leak/")
# txtToWav("../voice/", "1-80.txt")
# folders = ["4khz_data_no_leak", "4khz_data_leak"]
# doForAllFolders(folders, plot)
# txtToGraph("../", "analog02.csv")

