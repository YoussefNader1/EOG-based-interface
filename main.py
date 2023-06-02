# Imports
import os
from sklearn.model_selection import train_test_split
import signal_preprocessing as pp
import feature_extraction as fx
import models as m

# Read Files
path = "3-class"

list_of_classes = ["asagi", "kirp", "sag", "sol",
                   "yukari"]  # The classes name we interested in [down, blink, right, left, up]


def read_sig(folder_path):
    signals_f = []
    signals_name_f = []
    channel_f = []
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
                signals_f.append(temp_sig)  # list of signals N x 251 where N is number of signals in 3-class file
                signals_name_f.append(class_name)  # signal class ("asagi", "kirp", "sag", "sol", "yukari")
                break
    return signals_f, signals_name_f, channel_f


signals, signals_name, channel = read_sig(path)

signals_concat = []
signals_class_concat = []
for i in range(0, len(signals), 2):
    signals_concat.append(signals[i] + signals[i + 1])  # N x 250 (101 x 250)
    signals_class_concat.append(signals_name[i])

'''
recompute the sampling rate
'''
# preprocessing
filtered_signals = []
resampled_signals = []
removedDC_component_signals = []
for i in range(len(signals_concat)):
    # 1- Signals Filtering
    filtered_signals.append(
        pp.butter_bandpass_filter(signals_concat[i], Low_Cutoff=0.5, High_Cutoff=20.0, Sampling_Rate=176, order=2))
    # 2- Signals resampling
    resampled_signals.append(pp.Resampling(filtered_signals[i]))
    # 3- Signals DC removal
    removedDC_component_signals.append((pp.DC_removal(resampled_signals[i])))

# Normalize the signal
signal_normalized = pp.signal_normalize(removedDC_component_signals)

# Feature Extraction in Time Domain
# 1- using Auto Regressive
coefficients = fx.auto_regressive(signal_normalized)

# 2- using Max Peak
# peaks = fx.max_peak_values(signal_normalized)
# peaks_arr = np.array(peaks).reshape(-1, 1)

# 3 - wavelet
# ww = fx.wavelet_features(signal_normalized)

# 4 - PSD
# PSD_coeff = fx.psd_features(signal_normalized)

Y = pp.encoder(list_of_classes, signals_class_concat)

x_train, x_test, y_train, y_test = train_test_split(coefficients, Y, test_size=0.20, shuffle=True, random_state=42)

m.random_forest(x_train, y_train, x_test, y_test, "coef")
