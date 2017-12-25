import numpy as np
import os.path
import scipy.io.wavfile

def csvToWav(location, file_name, sample_rate=40000, skip=2):
    path = location + file_name
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
	folder = input("folder? (e.g. co2) ")
	location = '../' + folder + '/'
	file_name = input("file name? (e.g. analog05) ")
	file_name = file_name + '.csv'
	path = location + file_name

	# check whether path exist
	if os.path.exists(path) == False:
		print(path,'does not exist\n')
		continue

	while True:
		choice = input("use default setting?\nsample_rate = 40000\nskip first two line(maybe contains some informations like sample rate)\n[y/n]? ")
		if choice == 'y':
			csvToWav(location, file_name)
			break
		elif choice == 'n':
			# get sample rate
			sample_rate = int(input("sample rate? "))
		
			# get lines to skip
			skip = int(input("skip how many lines? "))
			csvToWav(location, file_name, sample_rate, skip)
			break
		else:
			print("accept only 'y' or 'n'")

