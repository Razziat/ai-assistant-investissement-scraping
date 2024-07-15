import pandas as pd
import matplotlib.pyplot as plt

# Charger les données à partir d'un fichier CSV
data = pd.read_csv('datas/actions_price_datas/all_categories/AIR.BE_full_monthly_data.csv')

# Convertir la colonne 'Month' en datetime pour faciliter le graphique
data['Month'] = pd.to_datetime(data['Month'])

# Filtrer pour garder uniquement les données à partir de janvier 2010
start_date = '2010-01-01'
data = data[data['Month'] >= pd.to_datetime(start_date)]

# Trier les données par mois pour s'assurer que le graphique est dans l'ordre chronologique
data.sort_values('Month', inplace=True)

# Création du graphique pour le 'Closing Price'
plt.figure(figsize=(10, 5))
plt.plot(data['Month'], data['Closing Price'], marker='o', linestyle='-', color='b', label='Closing Price')

# Ajouter des titres et labels
plt.title('Évolution du Closing Price par mois')
plt.xlabel('Mois')
plt.ylabel('Closing Price')
plt.xticks(rotation=45)
plt.legend()

# Afficher le graphique
plt.tight_layout()
plt.show()

# Création du graphique pour l' 'Opening Price'
plt.figure(figsize=(10, 5))
plt.plot(data['Month'], data['Opening Price'], marker='x', linestyle='--', color='r', label='Opening Price')

# Ajouter des titres et labels
plt.title('Évolution de l\'Opening Price par mois')
plt.xlabel('Mois')
plt.ylabel('Opening Price')
plt.xticks(rotation=45)
plt.legend()

# Afficher le graphique
plt.tight_layout()
plt.show()
