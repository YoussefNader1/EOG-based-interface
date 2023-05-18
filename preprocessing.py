import statistics
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import signal
from scipy.signal import butter, filtfilt


# 1) Filtering
def butter_bandpass_filter(Input_Signal, Low_Cutoff, High_Cutoff, Sampling_Rate, order):
    nyq = 0.5 * Sampling_Rate  # Nyquist Sampling
    low = Low_Cutoff / nyq
    high = High_Cutoff / nyq
    Numerator, denominator = butter(order, [low, high], btype='band', output='ba', analog=False, fs=None)
    # Passing the 1st Column of data shape (251,) instead of (251,1)
    filtered = filtfilt(Numerator, denominator, Input_Signal)
    return filtered



# 2) Resampling
def Resampling(filtered_Signal):
    resampled_Signal = signal.resample(filtered_Signal, 50)
    plt.figure(figsize=(12, 6))
    plt.subplot(121)
    plt.plot(np.arange(0, len(filtered_Signal)), filtered_Signal)
    plt.xlabel("Time(s)")
    plt.ylabel("Amp (v)")
    plt.subplot(122)
    plt.plot(np.arange(0, len(resampled_Signal)), resampled_Signal)
    plt.xlabel("Time(s)")
    plt.ylabel("Amp (v)")
    plt.show()


# 3) DC Remover
def DC_removal(filtered_Signal):
    DC_signal = [(filtered_Signal[i] + 10) for i in range(len(filtered_Signal))]
    Mean = statistics.mean(DC_signal)
    RemovedDC_signal = [(DC_signal[i] - Mean) for i in range(len(DC_signal))]
    plt.plot(np.arange(0, len(RemovedDC_signal)), RemovedDC_signal)
    plt.xlabel("Time (s)")
    plt.ylabel("Amp (v)")
    plt.show()