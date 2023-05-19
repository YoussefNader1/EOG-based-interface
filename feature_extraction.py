import openpyxl
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
from statsmodels.tsa.ar_model import AutoReg
from pylab import figure, clf, plot, xlabel, ylabel, title, grid, axes, show
from scipy.signal import find_peaks


def auto_regressive(signals):
    signal_coefficients = []
    for i in range(len(signals)):
        model = AutoReg(signals[i], lags=10)
        model_fit = model.fit()
        signal_coefficients.append(list(model_fit.params))
    return signal_coefficients