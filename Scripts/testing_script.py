import pickle
import os
from sklearn.metrics import accuracy_score
import main
import signal_preprocessing as pp
import feature_extraction as fx

# read data

folder_path = 'testing_data'


def read_sig(path):
    signals_f = []
    signals_name_f = []
    channel_f = []
    files = os.listdir(path)
    for file in files:
        temp_sig = []
        for class_name in main.list_of_classes:
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


signals, signals_name, channel = read_sig(folder_path)

signals_concat = []
signals_class_concat = []
for i in range(0, len(signals), 2):
    signals_concat.append(signals[i] + signals[i + 1])
    signals_class_concat.append(signals_name[i])

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

Y = pp.encoder(main.list_of_classes, signals_class_concat)


# load the model
def random_forest_test(x_testing, y_testing, feature_name):
    filename = 'rf_model' + feature_name + '.pkl'
    y_pred = []
    # Load the model if the file exists
    if os.path.exists(filename):
        with open(filename, 'rb') as file:
            rf_model = pickle.load(file)
            # Make predictions on the testing data
        y_pred = rf_model.predict(x_testing)

        # Evaluate the performance of the classifier
        accuracy = accuracy_score(y_testing, y_pred)
        print('Accuracy random forest using ' + feature_name + ": " + str(accuracy * 100))
        print('Random forest prediction values ', y_pred)
        print('Random forest Real values ', y_testing)

        print('Model loaded and used for prediction.')
    else:
        print('Model file does not exist.')

    return y_pred


def decision_tree(x_test, y_test, feature_name):
    filename = 'DT_model' + feature_name + '.pkl'
    y_pred = []
    # Load the model if the file exists
    if os.path.exists(filename):
        with open(filename, 'rb') as file:
            tree = pickle.load(file)

        # Make predictions on new data
        y_pred = tree.predict(x_test)
        accuracy = accuracy_score(y_test, y_pred)
        print('Accuracy DT using ' + feature_name + ": " + str(accuracy * 100))
        print('Decision tree prediction values ', y_pred)
        print('Decision tree Real values ', accuracy)
        print('Model loaded and used for prediction.')
    else:
        print('Model file does not exist.')

    return y_pred


# make prediction

"""
0 -> asagi -> down
1 -> krip -> blink
2 -> sag -> right
3 -> sol -> left
4 -> yukari -> up
"""

prediction = random_forest_test(coefficients, Y, "coef")

# we will get class name (up ,down ,right ,left)
orders = []

for i in prediction:
    if i == 0:
        orders.append('down')
    if i == 1:
        orders.append('blink')
    if i == 2:
        orders.append('right')
    if i == 3:
        orders.append('left')
    if i == 4:
        orders.append('top')

print(orders)
