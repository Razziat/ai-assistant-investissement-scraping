import os
from get_old_actions_data import run_for_ticker

"""
Launch get_old_actions_data.py on every symbol in actifs
"""

# Exemple de classification d'actifs
actifs = {
}

def save_data(category, ticker, data):
    # Crée le dossier s'il n'existe pas
    directory = f"datas/actions_price_datas/all_categories"
    if not os.path.exists(directory):
        os.makedirs(directory)
    # Sauvegarde les données dans un fichier CSV
    csv_file_name = f"{directory}/{ticker}_full_monthly_data.csv"
    data.to_csv(csv_file_name, index=False)
    print(f"Data for {ticker} saved in {csv_file_name}")

if __name__ == "__main__":
    for category, tickers in actifs.items():
        for ticker in tickers:
            try:
                data = run_for_ticker(ticker)
                save_data(category, ticker, data)
            except Exception as e:
                print(f"Failed to get data for {ticker}: {e}")