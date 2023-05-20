import openpyxl
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
from pylab import figure, clf, plot, xlabel, ylabel, title, grid, axes, show
from statsmodels.tsa.ar_model import AutoReg
from scipy.signal import find_peaks
import pywt

import numpy as np
from scipy import signal


def auto_regressive(signals):
    signal_coefficients = []
    for i in range(len(signals)):
        model = AutoReg(signals[i], lags=4)
        model_fit = model.fit()
        signal_coefficients.append(list(model_fit.params))
    return signal_coefficients


# acc 23% with DT
# 4% logistic
def max_peak_values(signals):
    Feature1 = []
    for sig in signals:
        peaks, _ = find_peaks(sig)
        X = []
        Y = []
        for i in range(len(peaks) - 1):
            L = (peaks[1])
            Y.append(sig[L])
            X.append(peaks[i])

        peak_value = max(Y)
        Feature1.append(peak_value)
    return Feature1


def wavelet_features(signals):
    signal_coefficients = []
    for i in range(len(signals)):
        # Apply wavelet transform to each signal
        coeffs = pywt.wavedec(signals[i], 'db4', level=3)

        # Extract features from wavelet coefficients
        features = []
        for j in range(len(coeffs)):
            cA = coeffs[j]
            cD = coeffs[j + 1] if j < len(coeffs) - 1 else None
            energy = sum(cA ** 2)
            entropy = -sum(cA ** 2 * np.log2(cA ** 2 + 1e-10))
            std = np.std(cA)
            features.extend([energy, entropy, std])
            if cD is not None:
                features.extend([np.mean(cD), np.std(cD)])

        signal_coefficients.append(features)

    return signal_coefficients


def psd_features(signals, fs=50):
    signal_coefficients = []
    for sig in signals:
        # Compute power spectral density using Welch's method
        f, Pxx = signal.welch(sig, fs=fs, nperseg=70, noverlap=65)

        # Extract features from the PSD
        features = []
        features.append(np.sum(Pxx))  # Total power
        features.append(np.sum(Pxx * f))  # Mean frequency
        features.extend(Pxx[:10])  # Top 10 PSD values
        signal_coefficients.append(features)

    return signal_coefficients
