import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from keras.models import Sequential, load_model
from keras.layers import Dense, LSTM
from sklearn.svm import SVR
from sklearn.preprocessing import MinMaxScaler

# Hyperparameters
window = 10

"""
This expects df_final.csv to be in the data/ directory.
If a TensorFlow LSTM model is present, it should also be in the data/ with name
bitcoin_tweet_predictor.h5
"""

def etl(filepath):
    dataset = pd.read_csv(filepath)
    dataset.columns = [x.lower() for x in dataset.columns]
    dataset["date"] = pd.to_datetime(dataset["date"])
    dataset = dataset.set_index("date")
    dataset = dataset.filter(["date", "count_negatives", "count_positives", "count_neutrals", "sent_negatives", "sent_positives", "close"])
    return dataset.dropna()

def normalize(X, y):
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaler = scaler.fit(X)
    X_normalized = scaler.transform(X)
    y = y.reshape(-1, 1)
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaler = scaler.fit(y)
    y_normalized = scaler.transform(y)
    return X_normalized, y_normalized

def denormalize(y_normalized, y_max, y_min):
    return y_normalized * (y_max - y_min) + y_min

def plot_data(X, y):
    fig, ax = plt.subplots(figsize=(16,8))
    ax.scatter(X[:, 0], y)
    ax.scatter(X[:, 1], y)
    return plt

def to_time_series(inputX, inputy):
    tsX, tsy = [], []
    for i in range(len(inputX) - window - 1):
        tsX.append(inputX[i : i + window])
        tsy.append(inputy[i + window - 1])
    return np.array(tsX), np.array(tsy)

def train_test_splitter(inputX, inputy, split=0.8):
    split = int(split * len(inputX))
    inputX_train, inputX_test = inputX[:split], inputX[split:]
    inputy_train, inputy_test = inputy[:split], inputy[split:]
    return inputX_train, inputX_test, inputy_train, inputy_test

def fit_lstm_model(X, y):
    try:
        model = load_model("data/bitcoin_tweet_predictor.h5")
    except:
        model = Sequential()
        model.add(LSTM(20, activation="relu", input_shape=(window, 5)))
        model.add(Dense(1))
        model.compile(loss="mean_squared_error", optimizer="sgd")
        model.fit(X, y, epochs=100, batch_size=10, verbose=2, validation_split=0.2)
        model.save("data/bitcoin_tweet_predictor.h5")
    return model

def predict(model, X):
    return model.predict(X)

def main():
    dataset = etl("data/df_final.csv")
    X = dataset.drop("close", axis=1).values
    y = dataset["close"].values
    X_normalized, y_normalized = normalize(X, y)
    tsX_normalized, tsy_normalized = to_time_series(X_normalized, y_normalized)
    tsX, tsy = to_time_series(X, y)
    tsX_norm_train, tsX_norm_test, tsy_norm_train, tsy_norm_test = train_test_splitter(tsX_normalized, tsy_normalized)
    _, _, _, tsy_test = train_test_splitter(tsX, tsy)
    tsy_test_max, tsy_test_min = np.max(tsy_test), np.min(tsy_test)
    model = fit_lstm_model(tsX_norm_train, tsy_norm_train)
    predictions_normalized = predict(model, tsX_norm_test)
    predictions = denormalize(predictions_normalized, tsy_test_max, tsy_test_min)
    tsy_test = np.reshape(tsy_test, (tsy_test.shape[0], 1))
    results = (np.array([predictions, tsy_test]).T)[0]
    np.savetxt("data/results.csv", results, delimiter=",")
    return results


if __name__ == "__main__":
    main()