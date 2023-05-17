# Imports
import os
import statistics

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import signal
from scipy.signal import butter, filtfilt

# Filtering
def butter_bandpass_filter(Input_Signal, Low_Cutoff, High_Cutoff, Sampling_Rate, order):
    nyq = 0.5 * Sampling_Rate  # Nyquist Sampling
    low = Low_Cutoff / nyq
    high = High_Cutoff / nyq
    Numerator, denominator = butter(order, [low, high], btype='band', output='ba', analog=False, fs=None)
    # Passing the 1st Column of data shape (251,) instead of (251,1)
    filtered = filtfilt(Numerator, denominator, Input_Signal)
    return filtered

# Read Files
path = "3-class"
signals = []
c = -1

for file in os.listdir(path):
    c += 1
    EOG_signal = open(path + "\\" + file, 'r')
    signals.append(EOG_signal.readlines())

sig = []
for i in range(len(signals)):
    temp = []
    for j in range(len(signals[0])-1):
        temp.append(int(signals[i][j + 1]))
    sig.append(temp)


# Preprocessing

# Signals Filtering
filtered_signal = []
for i in range(len(sig)):
    filtered_signal.append(butter_bandpass_filter(sig[i], Low_Cutoff=0.5, High_Cutoff=20.0, Sampling_Rate=176, order=2))

plt.figure(figsize=(12, 6))
plt.plot(np.arange(0, len(filtered_signal[0])), filtered_signal[0])
plt.xlabel("Time(s)")
plt.ylabel("Amp (v)")
plt.show()

# Signals Resampling
resampled_signals = []
for i in range(len(filtered_signal)):
    resampled_signals.append(signal.resample(filtered_signal[i], 50))

plt.figure(figsize=(12, 6))
plt.subplot(121)
plt.plot(np.arange(0, len(resampled_signals)), resampled_signals)
plt.xlabel("Time(s)")
plt.ylabel("Amp (v)")
plt.subplot(122)
plt.plot(np.arange(0, len(resampled_signals)), resampled_signals)
plt.xlabel("Time(s)")
plt.ylabel("Amp (v)")
plt.show()

# Signals DC Removal
RemovedDC_signals = []
DC_signal = [(resampled_signals[i] + 10) for i in range(len(resampled_signals))]
for i in range(len(DC_signal)):
    Mean = statistics.mean(DC_signal[i])
    RemovedDC_signals.append([(DC_signal[i] - Mean) for i in range(len(DC_signal))])

plt.plot(np.arange(0, len(RemovedDC_signals)), RemovedDC_signals[0])
plt.xlabel("Time (s)")
plt.ylabel("Amp (v)")
plt.show()



