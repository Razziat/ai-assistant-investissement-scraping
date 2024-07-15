import pandas as pd

# Charger les données financières
data_finance = pd.read_csv('path_to_your_finance_data.csv', parse_dates=['Month'], index_col='Month')

# Charger les données d'analyse de sentiment
data_sentiment = pd.read_csv('path_to_your_sentiment_analysis_results.csv', parse_dates=['Fichier'], index_col='Fichier')

# Nettoyage des données de sentiment pour éliminer les duplicatas (si 'resultats_analyse_sentiment.csv' est un duplicata)
data_sentiment = data_sentiment[~data_sentiment.index.str.contains('resultats_analyse_sentiment')]

# Convertir les indices de data_sentiment pour correspondre à ceux de data_finance
data_sentiment.index = data_sentiment.index.str.extract('(\d{4}-\d{2})')[0]
data_sentiment.index = pd.to_datetime(data_sentiment.index)

# Joindre les deux ensembles de données sur l'index de date
data_combined = pd.concat([data_finance, data_sentiment], axis=1, join='inner')
