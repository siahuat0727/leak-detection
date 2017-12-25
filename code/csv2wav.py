import numpy as np
import os.path
import scipy.io.wavfile

def csvToWav(path, sample_rate=40000, skip=2):
    if os.path.exists(path):
        wave = np.genfromtxt(path, dtype = np.int16)
        wave = np.asarray(wave)
        wave = wave[skip:]
        # wave = [x for i, x in enumerate(wave) if i %2==0]
        wave = np.array(wave)
        wave = 50 * (wave - int(np.mean(wave)))
        wave_path = path[:-3] + "wav"
        scipy.io.wavfile.write(wave_path, sample_rate, wave)
        print(wave_path + " is saved\n")
    else:
        print(path, "does not exist")


while True:
	print('\n**********convert csv to wav**********')

	# get path
	path = input("path? (e.g. ../co2/analog05.csv) ")

	# check whether path exist
	if os.path.exists(path) == False:
		print(path,'does not exist\n')
		continue

	while True:
		choice = input("use default setting?\nsample_rate = 40000\nskip first two line(maybe contains some informations like sample rate)\n[y/n]? ")
		if choice == 'y':
			csvToWav(path)
			break
		elif choice == 'n':
			# get sample rate
			sample_rate = int(input("sample rate? "))
		
			# get lines to skip
			skip = int(input("skip how many lines? "))
			csvToWav(path, sample_rate, skip)
			break
		else:
			print("accept only 'y' or 'n'")

