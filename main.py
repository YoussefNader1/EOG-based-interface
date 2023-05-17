# Imports
import os
import matplotlib.pyplot as pit
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy import signal
from scipy.signal import butter, filtfilt


# Read Files
path = "C:\\Users\\hooda\\PycharmProjects\\HCI\\3-class"
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

# # Draw signal
# plt.figure(figsize=(12, 6))
# plt.plot(np. arange(0, len(sig[0])), sig[0])
# plt.xlabel("Time (s)")
# plt.ylabel("Amp (v)")
# plt.show()
print()



