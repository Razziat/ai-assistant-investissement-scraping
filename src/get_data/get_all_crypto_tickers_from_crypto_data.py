import pandas as pd
import os

#Return the list of crypto symbol in file_path

file_path = 'src/get_data/crypto_data.csv'

# Vérifier si le fichier existe
if os.path.exists(file_path):
    try:
        data = pd.read_csv(file_path, encoding='utf-8')
        noms_des_investissements = data['tickers'].tolist()
        print(noms_des_investissements)
    except Exception as e:
        print(f"Une erreur s'est produite lors de la lecture du fichier : {e}")
else:
    print(f"Le fichier spécifié n'existe pas à l'emplacement : {file_path}")
