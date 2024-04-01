import pickle
from sklearn.metrics import accuracy_score
import signal_preprocessing as pp
import feature_extraction as fx
import serial

# Initialize serial communication with Arduino
ser = serial.Serial('/dev/cu.usbmodem1411', 115200)  # Adjust the port and baud rate as needed

# Load the trained model
with open('rf_modelcoef.pkl', 'rb') as file:
    rf_model = pickle.load(file)


# Define a function to preprocess and classify the incoming EOG signal
def classify_eog_signal(signal):
    # Preprocess the signal
    signal_normalized = pp.signal_normalize(signal)
    coefficients = fx.auto_regressive(signal_normalized)

    # Make predictions using the loaded model
    prediction = rf_model.predict(coefficients.reshape(1, -1))

    # Map predictions to meaningful actions (up/down movements in this case)
    if prediction == 0:
        return 'down'
    elif prediction == 4:
        return 'up'
    else:
        return 'unknown'


# Main loop to continuously read and classify EOG signals
while True:
    # Read data from Arduino
    raw_data = ser.readline().decode('utf-8').strip()

    # Process the raw data as needed (e.g., convert to integers)
    signal_data = [int(val) for val in raw_data.split(',')]

    # Classify the EOG signal
    movement = classify_eog_signal(signal_data)
    print('Predicted movement:', movement)
