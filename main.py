# Imports
import os
import statistics
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import signal
from scipy.signal import butter, filtfilt
import preprocessing as pp

# Read Files
path = "3-class"



def read_sig(folder_path):
    signals_f = []
    signals_name_f = []
    channel_f = []
    list_of_classes = ["asagi", "kirp", "sag", "sol", "yukari"]  # The classes name we interested in
    files = os.listdir(path)

    for file in files:
        temp_sig = []
        for class_name in list_of_classes:
            if file.startswith(class_name):
                name = file.split('.')
                channel_f.append(name[0][-1])  # list ['h' , 'v' , 'h' ,'v' , .....]
                with open(path + "\\" + file, 'r') as f:
                    for line in f:
                        s = line.strip()  # Remove the newline character
                        temp_sig.append(int(s))
                signals_f.append(temp_sig)  # list of signals N x 251 where N is number of signals
                signals_name_f.append(class_name)  # signal class ("asagi", "kirp", "sag", "sol", "yukari")
                break
    return signals_f, signals_name_f, channel_f


signals, signals_name, channel = read_sig(path)

