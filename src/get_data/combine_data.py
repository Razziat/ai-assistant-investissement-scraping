import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
from tensorflow.keras.metrics import RootMeanSquaredError

# Charger les données financières
data_finance = pd.read_csv('datas/actions_price_datas/all_categories/AIR.BE_full_monthly_data.csv', 
                           parse_dates=['Month'], 
                           index_col='Month')
data_finance = data_finance[data_finance.index >= '2010-01']

# Charger les données d'analyse de sentiment
data_sentiment = pd.read_csv('datas/resultats_analyse_sentiment_consolidés.csv')
data_sentiment['Month'] = pd.to_datetime(data_sentiment['Fichier'].str.extract('(\d{4}-\d{2})')[0])
data_sentiment = data_sentiment[~data_sentiment['Fichier'].str.contains('_resultats')]
data_sentiment.set_index('Month', inplace=True)
data_sentiment.drop(columns=['Fichier'], inplace=True)

# Jointure des données financières et de sentiment
data_combined = data_finance.join(data_sentiment, how='inner')

# Normalisation des prix de clôture
scaler = MinMaxScaler()
data_combined['Normalized Closing Price'] = scaler.fit_transform(data_combined[['Closing Price']])

# Préparation des données pour LSTM
def create_dataset(X, Y, time_steps=1):
    Xs, Ys = [], []
    for i in range(len(X) - time_steps):
        v = X.iloc[i:(i + time_steps)].values
        Xs.append(v)
        Ys.append(Y.iloc[i + time_steps])
    return np.array(Xs), np.array(Ys)

time_steps = 10
X, Y = create_dataset(data_combined[['Normalized Closing Price']], data_combined['Moyenne_Sentiment'], time_steps)

# Séparation des données
split = int(0.8 * len(X))
X_train, X_test = X[:split], X[split:]
Y_train, Y_test = Y[:split], Y[split:]

# Création du modèle LSTM
model = Sequential([
    LSTM(50, return_sequences=True, input_shape=[time_steps, X.shape[2]]),
    LSTM(50),
    Dense(1)
])
model.compile(loss='mean_squared_error', optimizer='adam', metrics=[RootMeanSquaredError()])
model.fit(X_train, Y_train, epochs=100, batch_size=32, verbose=1, validation_split=0.1)

# Prédictions futures
num_future_periods = 12  # Pour prédire 12 mois dans le futur
last_input = X[-1:]  # Dernier input de la séquence de données
future_predictions = []

for _ in range(num_future_periods):
    prediction = model.predict(last_input)
    future_predictions.append(prediction[0, 0])  # Ajouter la prédiction dénormalisée
    last_input = np.roll(last_input, -1)  # Décaler vers la gauche
    last_input[0, -1, 0] = prediction  # Mettre à jour le dernier élément avec la nouvelle prédiction

# Dénormaliser les prédictions futures
future_predictions = scaler.inverse_transform(np.array(future_predictions).reshape(-1, 1))

future_dates = pd.date_range(start=data_combined.index[-1] + pd.DateOffset(months=1), periods=num_future_periods, freq='M')

# Visualisation
plt.figure(figsize=(15, 8))
plt.plot(data_combined.index, scaler.inverse_transform(data_combined['Normalized Closing Price'].values.reshape(-1, 1)), label='Actual Closing Price')
plt.plot(future_dates, future_predictions, label='Predicted Future Price', linestyle='--')
plt.title('Future Stock Price Prediction for Airbus')
plt.xlabel('Time')
plt.ylabel('Price')
plt.legend()
plt.grid(True)
plt.show()
