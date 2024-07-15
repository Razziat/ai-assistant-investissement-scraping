import yfinance as yf
import pandas as pd
import pandas_ta as ta

def fetch_macd(symbol, start_date, end_date, fast_period=12, slow_period=26, signal_period=9):
    # Télécharger les données historiques du symbole
    data = yf.download(symbol, start=start_date, end=end_date)
    
    # Afficher les données téléchargées pour vérifier
    print("Données téléchargées:")
    print(data)
    
    # S'assurer que les données sont triées par date
    data.sort_index(inplace=True)
    
    # Calculer le MACD en utilisant pandas_ta
    macd = data.ta.macd(fast=fast_period, slow=slow_period, signal=signal_period, append=True)
    
    # Renvoyer le DataFrame contenant les données du MACD
    return macd

# Exemple d'utilisation
symbol = "AAPL"  # Symbole pour Apple Inc.
start_date = "2023-01-01"
end_date = "2023-12-31"

macd_data = fetch_macd(symbol, start_date, end_date)
print("Données MACD:")
print(macd_data)
