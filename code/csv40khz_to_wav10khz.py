import numpy as np
from os import listdir
from os.path import isfile, join
import os.path
import scipy.io.wavfile


def csvToWav(path, sample_rate=40000, skip=2, drop=4):
    if os.path.exists(path):
        wave = np.genfromtxt(path, dtype = np.int16)
        wave = np.asarray(wave)
        wave = wave[skip:]
        # wave = [x for i, x in enumerate(wave) if i%4 == 0]
        wave = np.array(wave)
        wave = 50 * (wave - int(np.mean(wave)))
        wave_path = path[:-3] + "wav"
        scipy.io.wavfile.write(wave_path, sample_rate, wave)
        print(wave_path + " is saved\n")
    else:
        print(path, "does not exist")

my_path = '../12_29_recorded'
if not os.path.exists(my_path):
	print(my_path, "DNE");
files = [f for f in listdir(my_path) if isfile(join(my_path, f))]
for f in files:
	csvToWav(my_path + '/' + f)

'''
while True:
	print('\n**********convert n kHz csv to n/drop kHz wav**********')

	# get path
	path = input("path? (e.g. ../co2/analog05.csv) ")

	# check whether path exist
	if os.path.exists(path) == False:
		print(path,'does not exist\n')
		continue

	while True:
		choice = input("use default setting?\nsample_rate = 40000\nskip first two line(maybe contains some informations like sample rate)\ndrop = 4\n[y/n]? ")
		if choice == 'y':
			csvToWav(path)
			break
		elif choice == 'n':
			# get sample rate
			sample_rate = int(input("sample rate? "))
		
			# get lines to skip
			skip = int(input("skip how many lines? "))

			#get drop
			drop = int(input("drop? (n to n/drop)"))
			csvToWav(path, sample_rate, skip, drop)
			brea
		else:
			print("accept only 'y' or 'n'")
'''
		
