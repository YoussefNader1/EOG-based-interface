import pickle
import os
from sklearn.metrics import accuracy_score
import main
import signal_preprocessing as pp
import feature_extraction as fx

# read data
x_test = []
y_test = []

path = 'testing_data'

signals, signals_name, channel = main.read_sig(path)

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
        print('Random forest prediction values ', y_test)

        print('Model loaded and used for prediction.')
    else:
        print('Model file does not exist.')


# make prediction


random_forest_test(coefficients, Y, "coef")

# we will get class name (up ,down ,right ,left)
