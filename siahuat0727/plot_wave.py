

#from . import feature_fft 
import numpy as np
import matplotlib.pyplot as plt
import itertools
import os.path
import scipy.io.wavfile
from scipy.fftpack import rfft, irfft, fftfreq

class Feature_fft(object):
    def __init__(self, sequence_data):
        self.data = sequence_data
        fft_trans = np.abs(np.fft.fft(sequence_data))
        self.dc = fft_trans[0]
        self.freq_spectrum = fft_trans[1:int(np.floor(len(sequence_data) * 1.0 / 2)) + 1]
        self._freq_sum_ = np.sum(self.freq_spectrum)

    def fft_dc(self):
        return self.dc

    def fft_mean(self):
        return np.mean(self.freq_spectrum)

    def fft_var(self):
        return np.var(self.freq_spectrum)

    def fft_std(self):
        return np.std(self.freq_spectrum)

    def fft_entropy(self):
        pr_freq = self.freq_spectrum * 1.0 / self._freq_sum_
        entropy = -1 * np.sum([np.log2(p) * p for p in pr_freq])
        return entropy

    def fft_energy(self):
        return np.sum(self.freq_spectrum ** 2) / len(self.freq_spectrum)

    # def fft_skew(self):
    #     fft_mean, fft_std = self.fft_mean(), self.fft_std()
    #     return np.mean([np.power((x - fft_mean) / fft_std, 3)
    #                     for x in self.freq_spectrum])
    def fft_skew(self):
        fft_mean, fft_std = self.fft_mean(), self.fft_std()

        return np.mean([0 if fft_std == 0 else np.power((x - fft_mean) / fft_std, 3)
                        for x in self.freq_spectrum])

    # def fft_kurt(self):
    #     fft_mean, fft_std = self.fft_mean(), self.fft_std()
    #     return np.mean([np.power((x - fft_mean) / fft_std, 4) - 3
    #                     for x in self.freq_spectrum])
    def fft_kurt(self):
        fft_mean, fft_std = self.fft_mean(), self.fft_std()
        return np.mean([0 if fft_std == 0 else np.power((x - fft_mean) / fft_std, 4) - 3
                        for x in self.freq_spectrum])

    def fft_max(self):
        idx = np.argmax(self.freq_spectrum)
        return idx, self.freq_spectrum[idx]

    def fft_topk_freqs(self, top_k=None):
        idxs = np.argsort(self.freq_spectrum)
        if top_k == None:
            top_k = len(self.freq_spectrum)
        return idxs[:top_k], self.freq_spectrum[idxs[:top_k]]

    # def fft_shape_mean(self):
    #     shape_sum = np.sum([x * self.freq_spectrum[x]
    #                         for x in range(len(self.freq_spectrum))])
    #     return shape_sum * 1.0 / self._freq_sum_
    def fft_shape_mean(self):
        shape_sum = np.sum([x * self.freq_spectrum[x]
                            for x in range(len(self.freq_spectrum))])
        return 0 if self._freq_sum_ == 0 else shape_sum * 1.0 / self._freq_sum_

    # def fft_shape_std(self):
    #     shape_mean = self.fft_shape_mean()
    #     var = np.sum([np.power((x - shape_mean), 2) * self.freq_spectrum[x]
    #                   for x in range(len(self.freq_spectrum))]) / self._freq_sum_
    #     return np.sqrt(var)
    def fft_shape_std(self):
        shape_mean = self.fft_shape_mean()
        var = np.sum([0 if self._freq_sum_ == 0 else np.power((x - shape_mean), 2) * self.freq_spectrum[x]
                      for x in range(len(self.freq_spectrum))]) / self._freq_sum_
        return np.sqrt(var)

    def fft_shape_skew(self):
        shape_mean = self.fft_shape_mean()
        return np.sum([np.power((x - shape_mean), 3) * self.freq_spectrum[x]
                       for x in range(len(self.freq_spectrum))]) / self._freq_sum_

    def fft_shape_kurt(self):
        shape_mean = self.fft_shape_mean()
        np.sum([np.power((x - shape_mean), 4) * self.freq_spectrum[x] - 3
                for x in range(len(self.freq_spectrum))]) / self._freq_sum_

    def fft_all(self):
        '''
        Get all fft features in one function
        :return: All fft features in one list
        '''
        feature_all = list()
        feature_all.append(self.fft_dc())
        feature_all.append(self.fft_shape_mean())
        feature_all.append(self.fft_shape_std() ** 2)
        feature_all.append(self.fft_shape_std())
        feature_all.append(self.fft_shape_skew())
        feature_all.append(self.fft_shape_kurt())
        feature_all.append(self.fft_mean())
        feature_all.append(self.fft_var())
        feature_all.append(self.fft_std())
        feature_all.append(self.fft_skew())
        feature_all.append(self.fft_kurt())
        return feature_all

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

def wavToGraph(location, file_name):
    path = location + file_name
    if os.path.exists(path):
        with open(path) as f:
            sample_rate, data = scipy.io.wavfile.read(path)
            time = np.linspace(0, data.size//sample_rate, data.size)
            plt.plot(time, data)
            plt.show()
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
            subPlotFFT(location1, file_name)
            # subPlotFFT(location2, file_name)
            # subPlotFFT2(location1, location2, file_name)
    plt.show()

# compareTwoFolders("../4khz_data_no_leak/", "../4khz_data_leak/")
# txtToWav("../voice/", "1-80.txt")
# folders = ["4khz_data_no_leak", "4khz_data_leak"]
# doForAllFolders(folders, plot)
# wavToGraph("./", "analog01.wav")


with open("analog01.wav") as f:
    sample_rate, data = scipy.io.wavfile.read("analog01.wav")
    obj = Feature_fft(data)
    print(obj.fft_all())
    fft_trans = np.abs(np.fft.fft(data))
    print(obj.dc)
    plt.plot(obj.freq_spectrum)
    plt.show()
