import openpyxl
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
from statsmodels.tsa.ar_model import AutoReg
from pylab import figure, clf, plot, xlabel, ylabel, title, grid, axes, show
from scipy.signal import find_peaks


def Auto_Regressive(signals):

    for i in range(len(signals)):
        signals_values = signals[i]
        signal = []
        for a in signals_values:
            signal.append(a.value)
        print(signal)
        model = AutoReg(signal, lags=4)
        model_fit = model.fit()
        print('coefficients: %s' % model_fit.params)
        plt.figure(figsize=(12, 6))
        plt.plot(np.arange(0, len(signal)), signal)
        plt.xlabel("Time")
        plt.ylabel('Amp')
        plt.show()
