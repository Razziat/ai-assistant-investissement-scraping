import pandas as pd
from transformers import BertTokenizer, BertForSequenceClassification
from transformers import pipeline

# Charger le modèle et le tokenizer FinBERT
model_name = "yiyanghkust/finbert-tone"
tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)

# Initialiser la pipeline d'analyse de sentiment
nlp = pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)

# Charger le fichier CSV
df = pd.read_csv('datas/articles/articles_Airbus_2013-01.csv')

mots_cles_inappropriés = ['cookie', 'consentement', 'privacy', 'GDPR', 'subscription']
df_filtre = df.copy()

for mot in mots_cles_inappropriés:
    df_filtre = df_filtre[~df_filtre['Contenu'].str.contains(mot, case=False, na=False)]

# S'assurer que le fichier contient les colonnes 'Titre' et 'Contenu'
if not {'Titre', 'Contenu'}.issubset(df_filtre.columns):
    raise ValueError("Le fichier CSV doit contenir les colonnes 'Titre' et 'Contenu'.")

# Fonction pour calculer le sentiment d'un texte
def calculer_sentiment_finbert(texte, titre):
    if pd.isna(texte) or texte.strip() == '':
        texte_a_analyser = titre  # Utiliser le titre si le contenu est vide
    else:
        texte_a_analyser = texte  # Sinon, utiliser le contenu
    # Tokeniser le texte et tronquer si nécessaire
    tokens = tokenizer.tokenize(texte_a_analyser)
    tokens = tokens[:509]  # Réduire à 509 tokens pour laisser de la place pour [CLS] et [SEP]
    texte_tronque = tokenizer.convert_tokens_to_string(tokens)
    # Effectuer l'analyse de sentiment sur le texte tronqué
    return nlp(texte_tronque)[0]

# Appliquer l'analyse de sentiment FinBERT
df_filtre['sentiment_finbert'] = df_filtre.apply(lambda x: calculer_sentiment_finbert(x['Contenu'], x['Titre']), axis=1)

# Uniformiser la casse des labels de sentiment
df_filtre['sentiment_label'] = df_filtre['sentiment_finbert'].apply(lambda x: x['label'].lower())

# Extraire le score de sentiment
df_filtre['sentiment_score'] = df_filtre['sentiment_finbert'].apply(lambda x: x['score'])

# Calculer la moyenne des scores de sentiment
df_filtre['sentiment_numerique'] = df_filtre['sentiment_label'].map({'positive': 1, 'neutral': 0, 'negative': -1})
print(df_filtre['sentiment_label'].value_counts())

moyenne_sentiment = df_filtre['sentiment_numerique'].mean()
moyenne_score_confiance = df_filtre['sentiment_score'].mean()

if moyenne_sentiment >= 0.66 :
    label_moyen = "Positif+"
elif moyenne_sentiment < 0.66 and moyenne_sentiment >= 0.33:
    label_moyen = "Positif"
elif moyenne_sentiment < 0.33 and moyenne_sentiment > 0:
    label_moyen = "Positif-"
elif moyenne_sentiment == 0:
    label_moyen = "Neutre"
elif moyenne_sentiment < 0 and moyenne_sentiment >= -0.33:
    label_moyen = "Negative+"
elif moyenne_sentiment < -0.33 and moyenne_sentiment >= -0.66:
    label_moyen = "Negative"
else:
    label_moyen = "Negative-"

# Afficher la moyenne du sentiment
print(f"Moyenne du sentiment sur tous les articles filtrés : {moyenne_sentiment} ({label_moyen})")
print(f"Moyenne du score de confiance : {moyenne_score_confiance}")

# Sauvegarder le DataFrame filtré dans un nouveau fichier CSV
chemin_fichier_sortie = 'datas/resultats_analyse_sentiment_filtres.csv'
df_filtre.to_csv(chemin_fichier_sortie, index=False)

print(f"Les résultats filtrés ont été sauvegardés dans {chemin_fichier_sortie}")

"""
Il faudrait prendre en compte les resultats des mois précédents (x - n mois) dans le calcul du cours du mois x.
Parfois il y a plus d'articles positifs que négatifs (12/2017 26 + contre 4 -) et pourtant le cours de l'action a légèrement baissé
"""