from pylab import *
import wave

sig = wave.open('1-20-minus.wav','r')
xsig = sig.readframes(-1)
xsig = fromstring(xsig, 'Int16')
f = sig.getframerate()
spectrogram = specgram(xsig[0:300000], Fs = f, scale_by_freq=True,sides='default')
axis('tight')
title('Spectrogram of Sound Synthesis Variant 2, with Python');
show()
sig.close()
