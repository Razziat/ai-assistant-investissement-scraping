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
        print(f"Erreur lors de la récupération de l'article pour {url}: {e}")
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

def filtrer_articles_financiers(articles):
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
    'data breach', 'hack', 'leak', 'espionage', 'embargo', 'sanction'
    ]

    articles_financiers = []

    for article in articles:
        if any(mot_cle in article['Contenu'].lower() for mot_cle in mots_cles_financiers):
            articles_financiers.append(article)

    return pd.DataFrame(articles_financiers)

noms_entreprises = [
    "ACCOR", "AIR LIQUIDE", "AIRBUS", "ARCELORMITTAL", "AXA", "BNP PARIBAS", "BOUYGUES",
    "CAPGEMINI", "CARREFOUR", "CREDIT AGRICOLE", "DANONE", "DASSAULT SYSTEMES", "EDENRED",
    "ENGIE", "ESSILORLUXOTTICA", "EUROFINS SCIENTIF", "HERMES INTL", "KERING", "L'OREAL",
    "LEGRAND", "LVMH", "MICHELIN", "ORANGE", "PERNOD-RICARD", "PUBLICIS GROUPE", "RENAULT",
    "SAFRAN", "SAINT-GOBAIN", "SANOFI", "SCHNEIDER ELECTRIC", "SOCIETE GENERALE", "STELLANTIS NV",
    "STMICROELECTRONICS", "TELEPERFORMANCE", "THALES", "TOTALENERGIES", "UNIBAIL RODAMCO UN",
    "VEOLIA ENVIRONNEME", "VINCI", "VIVENDI"
]

start_period = datetime(2010, 1, 1)
end_period = datetime(2024, 3, 31)
date_range = pd.date_range(start=start_period, end=end_period, freq='MS')

for keyword in noms_entreprises:
    print(f"Recherche d'articles pour : {keyword}")
    for start_date in date_range:
        end_date = start_date + pd.offsets.MonthEnd()
        start_date_tuple = (start_date.year, start_date.month, start_date.day)
        end_date_tuple = (end_date.year, end_date.month, end_date.day)

        articles_df = rechercher_articles(keyword, start_date_tuple, end_date_tuple)
        articles_financiers_df = filtrer_articles_financiers(articles_df.to_dict('records'))

        
        if not articles_financiers_df.empty:
            chemin_csv = f"articles_{keyword.replace(' ', '_')}_{start_date.strftime('%Y-%m')}.csv"
            articles_financiers_df.to_csv(chemin_csv, index=False)
            print(f"Les articles pour {keyword} ont été sauvegardés dans le fichier '{chemin_csv}'.")
        else:
            print(f"Aucun article trouvé pour {keyword} dans la période {start_date.date()} - {end_date.date()}.")
