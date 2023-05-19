# Imports
import os
import statistics
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import signal
from scipy.signal import butter, filtfilt
from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn import metrics
import signal_preprocessing as pp
import feature_extraction as fx
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC

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

# preprocessing
filtered_signals = []
resampled_signals = []
removedDC_component_signals = []
for i in range(len(signals)):
    # 1- Signals Filtering
    filtered_signals.append(
        pp.butter_bandpass_filter(signals[i], Low_Cutoff=0.5, High_Cutoff=20.0, Sampling_Rate=176, order=2))
    # 2- Signals resampling
    resampled_signals.append(pp.Resampling(filtered_signals[i]))
    # 3- Signals DC removal
    removedDC_component_signals.append((pp.DC_removal(resampled_signals[i])))

# Concatenation of the horizontal and vertical channels into one signal
signals_concat = []
signals_class_concat = []
for i in range(0, len(signals), 2):
    signals_concat.append(removedDC_component_signals[i] + removedDC_component_signals[i + 1])  # N x 250 (101 x 250)
    signals_class_concat.append(signals_name[i])

# Normalize the signal (0 -> 1)
signal_normalized = pp.signal_normalize(signals_concat)

# Feature Extraction in Time Domain
# 1- using Auto Regressive
coefficients = fx.auto_regressive(signals_concat)

# 2- using Max Peak
# peaks = fx.max_peaks(signals_concat)

Y = pp.encoder(list_of_classes, signals_class_concat)

x_train, x_test, y_train, y_test = train_test_split(signals_concat, Y, test_size=0.20, shuffle=True, random_state=1)



# Create a logistic regression model
logreg = LogisticRegression()

# Fit the model to the data
logreg.fit(x_train, y_train)

# Make predictions on the training data
y_pred = logreg.predict(x_test)

# Calculate the accuracy of the model
accuracy = accuracy_score(y_test, y_pred)

print("Accuracy: {:.2f}%".format(accuracy * 100))
#
# print('----------')
from sklearn.tree import DecisionTreeClassifier

# Assuming 'X' is your input data (a 2D numpy array or pandas DataFrame) and 'y' is your target variable (a 1D numpy array or pandas Series)

# Create a decision tree model
tree = DecisionTreeClassifier()

# Fit the model to the data
tree.fit(x_train, y_train)

# Make predictions on new data
y_pred = tree.predict(x_test)
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy: {:.2f}%".format(accuracy * 100))


# from sklearn.preprocessing import LabelEncoder
# from keras.utils import to_categorical

# Encode the target variable as integers
# encoder = LabelEncoder()
# encoder.fit(Y)
# y_encoded = encoder.transform(Y)
#
# # Convert the target variable to one-hot vectors
# y_onehot = to_categorical(y_encoded)

# Split the data into training and testing sets
# x_train, x_test, y_train, y_test = train_test_split(signals_concat, y_onehot, test_size=0.20, shuffle=True, random_state=1)

# Build and train a neural network model
# from keras.models import Sequential
# from keras.layers import Dense
#
# # Define a neural network model
# model = Sequential()
# model.add(Dense(16, input_dim=x_train.shape[1], activation='relu'))
# model.add(Dense(8, activation='relu'))
# model.add(Dense(Y.shape[1], activation='softmax'))
#
# # Compile the model
# model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
#
# # Train the model on the training data
# model.fit(x_train, y_train, epochs=50, batch_size=32)
#
# # Evaluate the model on the testing data
# loss, accuracy = model.evaluate(x_test, y_test)
# print('Test loss:', loss)
# print('Test accuracy:', accuracy)
