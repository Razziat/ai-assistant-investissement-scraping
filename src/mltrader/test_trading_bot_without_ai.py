import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def fetch_data(symbol, start_date, end_date):
    data = yf.download(symbol, start=start_date, end=end_date)
    print("Données brutes récupérées:")
    print(data.head())
    return data

# Récupération des données
eur_usd_data = fetch_data("EURUSD=X", "2020-01-01", "2022-01-01")

def calculate_sma(data, window):
    sma = data['Close'].rolling(window=window).mean()
    return sma

# Calcul de la SMA sur 50 jours
eur_usd_data['SMA_50'] = calculate_sma(eur_usd_data, 50)

def calculate_sma(data, window):
    return data['Close'].rolling(window=window).mean()

# Correction du calcul du RSI pour gérer les divisions par zéro
def calculate_rsi(data, periods=14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
    rs = gain / (loss.replace(0, np.nan))  # éviter la division par zéro en remplaçant 0 par NaN
    return 100 - (100 / (1 + rs))

# Ajustement des paramètres de la SMA
eur_usd_data['SMA_20'] = calculate_sma(eur_usd_data, 20)  # Période plus courte
eur_usd_data['RSI'] = calculate_rsi(eur_usd_data, 14)  # RSI standard

def generate_signals(data):
    signals = pd.DataFrame(index=data.index)
    signals['signal'] = 0.0
    # Utilisation des seuils RSI modifiés pour vérifier si les signaux peuvent être générés
    signals.loc[(data['Close'] > data['SMA_20']) & (data['RSI'] < 30), 'signal'] = 1.0
    signals.loc[(data['Close'] < data['SMA_20']) & (data['RSI'] > 70), 'signal'] = -1.0
    signals['positions'] = signals['signal'].diff()
    return signals

eur_usd_signals = generate_signals(eur_usd_data)

def backtest(data, signals):
    if data.empty or signals.empty:
        print("Aucune donnée pour effectuer le backtest.")
        return pd.DataFrame()
    initial_capital = float(10000.0)
    positions = pd.DataFrame(index=signals.index).fillna(0.0)
    portfolio = pd.DataFrame(index=signals.index).fillna(0.0)

    # Acheter ou vendre 1000 unités basées sur le signal
    positions['EUR/USD'] = 1000 * signals['signal']
    portfolio['positions'] = positions['EUR/USD'] * data['Close']
    portfolio['cash'] = initial_capital - (positions.diff()['EUR/USD'] * data['Close']).cumsum()

    # Initialiser le premier jour correctement si nécessaire
    if not portfolio.empty:
        first_index = portfolio.index[0]
        portfolio.loc[first_index, 'cash'] = initial_capital - positions.loc[first_index, 'EUR/USD'] * data.loc[first_index, 'Close']
    portfolio['total'] = portfolio['positions'] + portfolio['cash']
    portfolio['returns'] = portfolio['total'].pct_change()

    return portfolio

eur_usd_portfolio = backtest(eur_usd_data, eur_usd_signals)

if not eur_usd_portfolio.empty:
    # Calcul du rendement total
    if np.isnan(eur_usd_portfolio['total'].iloc[-1]) or np.isnan(eur_usd_portfolio['total'].iloc[0]):
        print("Impossible de calculer le rendement total en raison de valeurs NaN")
    else:
        total_return = eur_usd_portfolio['total'].iloc[-1] - eur_usd_portfolio['total'].iloc[0]
        print("Rendement total:", total_return)
    
    # Calcul du ratio de Sharpe et du drawdown maximal
    expected_return = eur_usd_portfolio['returns'].mean()
    return_std = eur_usd_portfolio['returns'].std()
    sharpe_ratio = (expected_return / return_std) * np.sqrt(252)
    print("Ratio de Sharpe:", sharpe_ratio)
    max_drawdown = eur_usd_portfolio['total'].div(eur_usd_portfolio['total'].cummax()).sub(1).min()
    print("Drawdown maximal:", max_drawdown)

plt.figure(figsize=(15, 7))
plt.plot(eur_usd_data['Close'], label='Prix de clôture')
plt.plot(eur_usd_data['SMA_50'], label='Moyenne Mobile 50 jours', color='orange')
plt.scatter(eur_usd_signals[eur_usd_signals['positions'] == 1].index, eur_usd_data['Close'][eur_usd_signals['positions'] == 1], color='green', label='Achat', marker='^', alpha=0.7)
plt.scatter(eur_usd_signals[eur_usd_signals['positions'] == -1].index, eur_usd_data['Close'][eur_usd_signals['positions'] == -1], color='red', label='Vente', marker='v', alpha=0.7)
plt.title('EUR/USD Prix de Clôture et SMA 50 avec Signaux de Trading')
plt.legend()
plt.show()
