#!/usr/bin/env python3

# sudo pip install PeakUtils

import numpy as np
import sounddevice as sd
import soundfile   as sf
import matplotlib.pyplot as plt

from scipy.fftpack import fft
from scipy import signal

def generateSin(freq, amplitude, time, fs):
        n = time*fs
        x = np.linspace(0.0, time, n)
        s = amplitude*np.sin(freq*x*2*np.pi)
        return (x, s)

def calcFFT(signal, fs):
        # https://docs.scipy.org/doc/scipy/reference/tutorial/fftpack.html
        N  = len(signal)
        T  = 1/fs
        xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
        yf = fft(signal)
        return(xf, yf[0:N//2])

def LPF(signal, cutoff_hz, fs):
        from scipy import signal as sg
        #####################
        # Filtro
        #####################
        # https://scipy.github.io/old-wiki/pages/Cookbook/FIRFilter.html
        nyq_rate = fs/2
        width = 5.0/nyq_rate
        ripple_db = 60.0 #dB
        N , beta = sg.kaiserord(ripple_db, width)
        taps = sg.firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))
        return( sg.lfilter(taps, 1.0, signal))

def main():
    fs = 44100
    sd.default.samplerate = fs
    sd.default.channels = 1
    audio, samplerate = sf.read('camFis.wav')
    yAudio = audio[:,1]
    samplesAudio = len(yAudio)
    
    #####################
    # Normaliza audio
    #####################
    audioMax = np.max(np.abs(yAudio))
    yAudioNormalizado = yAudio/audioMax

    plt.figure("tempo")
    plt.plot(yAudioNormalizado)
    plt.grid()
    plt.title('Oi no tempo')

    #####################
    # Filtro
    #####################
    # https://scipy.github.io/old-wiki/pages/Cookbook/FIRFilter.html
    nyq_rate = samplerate/2
    width = 5.0/nyq_rate
    ripple_db = 60.0 #dB
    N , beta = signal.kaiserord(ripple_db, width)
    cutoff_hz = 1000.0
    taps = signal.firwin(N, cutoff_hz/nyq_rate, window=('kaiser', beta))

    #####################
    # Aplica filtro no sinal
    #####################
    print("nao filtrado")
    sd.play(yAudio)
    sd.wait()
    yFiltrado = LPF(yAudioNormalizado, 2000, samplerate)
    print("filtrado")
    sd.play(yFiltrado)
    sd.wait()

if __name__ == "__main__":
    main()
