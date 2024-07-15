import pandas as pd
import statsmodels.api as sm
import glob

def charger_et_preparer_les_donnees(chemin_fichiers_sentiment, chemin_fichier_prix):
    # Charger les données de sentiment
    df_sentiment = pd.concat([pd.read_csv(f) for f in glob.glob(chemin_fichiers_sentiment)], ignore_index=True)
    df_sentiment['Month'] = pd.to_datetime(df_sentiment['Fichier'].str.extract(r'_(\d{4}-\d{2})')[0])

    # Charger les données des prix d'ouverture
    df_prix = pd.read_csv(chemin_fichier_prix)
    df_prix['Month'] = pd.to_datetime(df_prix['Month'])

    # Fusionner les données sur le mois
    df_combined = pd.merge(df_sentiment, df_prix[['Month', 'Opening Price']], on='Month', how='inner')
    
    return df_combined

def calculer_correlation_et_regresser(df):
    # Calcul de la corrélation
    correlation = df['Moyenne_Sentiment'].corr(df['Opening Price'])
    print(f"Corrélation entre la moyenne du sentiment et le prix d'ouverture: {correlation}")

    # Régression linéaire
    X = df[['Moyenne_Sentiment']]
    y = df['Opening Price']
    X = sm.add_constant(X)  # ajouter une constante
    
    model = sm.OLS(y, X).fit()
    predictions = model.predict(X)
    
    print(model.summary())

if __name__ == "__main__":
    chemin_fichiers_sentiment = 'datas/resultats_analyse_sentiment_consolidés.csv'
    chemin_fichier_prix = 'datas/actions_price_datas/all_categories/AIR.BE_full_monthly_data.csv'

    # Charger et préparer les données
    df_combined = charger_et_preparer_les_donnees(chemin_fichiers_sentiment, chemin_fichier_prix)
    
    # Calculer la corrélation et effectuer la régression
    calculer_correlation_et_regresser(df_combined)
