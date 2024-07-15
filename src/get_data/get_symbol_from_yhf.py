import csv

def lire_actions_depuis_txt_et_enregistrer(file_path, csv_path):
    # Ouvrir le fichier en mode lecture avec l'encodage UTF-8
    with open(file_path, 'r', encoding='utf-8') as file:
        # Lire le contenu du fichier
        contenu = file.read()
        
        # Évaluer le contenu pour obtenir le dictionnaire
        dictionnaire_actions = eval(contenu)
        
        # Extraire les symboles des actions
        liste_actions = list(dictionnaire_actions.keys())
    
    # Préparer les symboles pour le formatage CSV
    symboles_format_csv = [f"'{symbole}'" for symbole in liste_actions]
    
    # Convertir en une seule chaîne de caractères avec des virgules
    chaine_symboles = ", ".join(symboles_format_csv)
    
    # Enregistrer dans un fichier CSV
    with open(csv_path, 'w', encoding='utf-8') as fichier_csv:
        fichier_csv.write(chaine_symboles)

# Chemin vers votre fichier txt
file_path = 'src/get_data/yhallsym.txt'
csv_path = 'src/get_data/result_yhallsym.csv'

lire_actions_depuis_txt_et_enregistrer(file_path, csv_path)