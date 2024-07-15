from gnews import GNews
from newspaper import Article
import pandas as pd
from datetime import datetime

def recuperer_contenu_complet(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        print(f"Erreur lors de la récupération de l'article : {e}")
        return ""

def rechercher_articles(keyword, start_date, end_date):
    google_news = GNews(language='en', country='US')
    google_news.start_date = start_date
    google_news.end_date = end_date
    google_news.max_results = 100

    articles = google_news.get_news(keyword)
    articles_liste = []

    for article in articles:
        titre = article.get('title')
        date_publication = article.get('published date')
        url = article.get('url')
        contenu = recuperer_contenu_complet(url)

        articles_liste.append({
            'Titre': titre,
            'Date de publication': date_publication,
            'URL': url,
            'Contenu': contenu
        })

    return pd.DataFrame(articles_liste)

"""def filtrer_articles_financiers(articles):
    mots_cles_financiers = [
    'finance', 'investment', 'stock market', 'shares', 'equity', 'bond',
    'dividend', 'portfolio', 'capital', 'market cap', 'trading',
    'financial statements', 'IPO', 'merger', 'acquisition', 'hedge fund',
    'mutual fund', 'ETF', 'liquidity', 'volatility', 'bull market',
    'bear market', 'index fund', 'fiscal year', 'quarterly report',
    'earnings', 'profit margin', 'revenue', 'debt', 'leverage',
    'bankruptcy', 'valuation', 'asset management', 'credit rating',
    'interest rate', 'yield', 'ROI', 'risk management', 'commodity',
    'derivative', 'option', 'futures', 'short selling', 'financial analysis',
    'economic indicators', 'monetary policy', 'fiscal policy', 'inflation',
    'GDP', 'foreign exchange', 'contract', 'agreement', 'partnership',
    'collaboration', 'deal', 'launch', 'innovation', 'patent', 'regulation',
    'compliance', 'litigation', 'lawsuit', 'recall', 'safety', 'incident',
    'accident', 'malfunction', 'failure', 'disruption', 'risk', 'penalty',
    'fine', 'settlement', 'arbitration', 'negotiation', 'divestiture',
    'expansion', 'growth', 'downturn', 'restructuring', 'downsizing',
    'layoff', 'strike', 'protest', 'scandal', 'controversy', 'fraud',
    'embezzlement', 'corruption', 'investigation', 'cybersecurity',
    'data breach', 'hack', 'leak', 'espionage', 'embargo', 'sanction', 'cyberattack',
    'CEO resignation', 'executive scandal', 'product recall', 'sustainability report',
    'ESG rating', 'corporate governance', 'brand reputation', 'consumer boycott',
    'data privacy', 'labor dispute', 'supply chain disruption', 'environmental impact',
    'social responsibility', 'political tension', 'regulatory approval', 'patent infringement',
    'merger rumors', 'product launch', 'technology breakthrough', 'market entry'
    ]

    articles_financiers = []

    for article in articles:
        if any(mot_cle in article['Contenu'].lower() for mot_cle in mots_cles_financiers):
            articles_financiers.append(article)

    return pd.DataFrame(articles_financiers)"""

if __name__ == "__main__":
    keyword = "Airbus"
    start_period = datetime(2010, 1, 1)
    end_period = datetime(2024, 3, 31)

    # Générer des plages de dates mensuelles
    date_range = pd.date_range(start=start_period, end=end_period, freq='MS')

    for start_date in date_range:
        # Calculer la fin du mois
        end_date = start_date + pd.offsets.MonthEnd()
        print(f"Recherche d'articles pour la période : {start_date.date()} - {end_date.date()}")

        # Convertir les dates en tuples (année, mois, jour)
        start_date_tuple = (start_date.year, start_date.month, start_date.day)
        end_date_tuple = (end_date.year, end_date.month, end_date.day)

        # Récupérer les articles pour la période courante
        articles_df = rechercher_articles(keyword, start_date_tuple, end_date_tuple)
        #articles_financiers_df = filtrer_articles_financiers(articles_df.to_dict('records'))
        
        if not articles_df.empty:
            chemin_csv = f"datas/articles_whithout_filter/articles_{keyword}_{start_date.strftime('%Y-%m')}.csv"
            articles_df.to_csv(chemin_csv, index=False)
            print(f"Les articles ont été sauvegardés dans le fichier '{chemin_csv}'.")
        else:
            print("Aucun article trouvé pour cette période.")
