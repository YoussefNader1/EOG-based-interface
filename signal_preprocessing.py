import statistics
import numpy as np
from scipy import signal
from scipy.signal import butter, filtfilt
from sklearn import preprocessing


def encoder(classes, signal_names):
    le = preprocessing.LabelEncoder()
    le.fit(classes)
    return list(le.transform(signal_names))


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
    resampled_Signal = signal.resample(filtered_Signal, 80)
    return list(resampled_Signal)


# 3) DC Remover
def DC_removal(filtered_Signal):
    DC_signal = [(filtered_Signal[i] + 10) for i in range(len(filtered_Signal))]
    Mean = statistics.mean(DC_signal)
    RemovedDC_signal = [(DC_signal[i] - Mean) for i in range(len(DC_signal))]
    return RemovedDC_signal


# 4) Normalization
def signal_normalize(data):
    # Convert the input list to a numpy array
    arr_data = np.array(data)

    # Normalize the data along the second axis (columns)
    normalized_data = preprocessing.normalize(arr_data, axis=1)

    # Convert the normalized numpy array back to a list of lists
    nl = normalized_data.tolist()

    return nl
