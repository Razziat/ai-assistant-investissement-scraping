import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

data = pd.read_csv('datas/resultats_analyse_sentiment_consolidés.csv')

# Fonction pour extraire et convertir la date
def extract_date(filename):
    try:
        # Extrait la partie qui devrait contenir la date
        date_part = Path(filename).stem.split('_')[-1]
        # Convertit en datetime si cela ressemble à une date YYYY-MM
        if len(date_part) == 7 and date_part[4] == '-':
            return pd.to_datetime(date_part)
    except ValueError:
        # Retourne None si la conversion échoue
        return None

# Appliquer la fonction d'extraction de date
data['Date'] = data['Fichier'].apply(extract_date)

# Supprimer les lignes où la date n'a pas pu être extraite
data = data.dropna(subset=['Date'])

# Grouper par date et calculer la moyenne des sentiments pour chaque mois
# Note: Si chaque mois est unique, cette étape peut être simplifiée
grouped_data = data.groupby('Date')['Moyenne_Sentiment'].mean().reset_index()

# Trier les données par date pour s'assurer que le graphique est dans l'ordre chronologique
grouped_data.sort_values('Date', inplace=True)

# Création du graphique linéaire
plt.figure(figsize=(10, 5))
plt.plot(grouped_data['Date'], grouped_data['Moyenne_Sentiment'], marker='o', linestyle='-', color='green')

# Ajouter des titres et labels
plt.title('Évolution de la Moyenne Sentiment par mois')
plt.xlabel('Mois')
plt.ylabel('Moyenne Sentiment')
plt.xticks(rotation=45)
plt.grid(True)

# Afficher le graphique
plt.tight_layout()
plt.show()
