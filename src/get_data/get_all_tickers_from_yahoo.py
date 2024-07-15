from YahooTickerDownloader import TickerDownloader
import pandas as pd

def telecharger_symboles():
    downloader = TickerDownloader()

    # Modifier le type de symbole si nécessaire, par exemple 'etf', 'future', 'index', etc.
    symboles = downloader.download('equity')

    # Préparation de la liste pour le DataFrame
    data = []
    for symbole in symboles:
        data.append(symbole)

    # Création d'un DataFrame
    df = pd.DataFrame(data)

    # Sauvegarde dans un fichier CSV
    df.to_csv('symboles_yahoo_finance.csv', index=False)

# Appel de la fonction
telecharger_symboles()
