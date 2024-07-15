import requests
from bs4 import BeautifulSoup

def rechercher_articles_google_news(entreprise, articles_deja_traites=set()):
    entreprise = entreprise.replace(' ', '+')
    url = f"https://news.google.com/search?q={entreprise}&hl=fr&gl=FR&ceid=FR:fr"
    reponse = requests.get(url)
    soup = BeautifulSoup(reponse.content, 'html.parser')
    articles = soup.findAll('article')
    resultats = []
    for article in articles:  # Retirer la limite pour s'assurer d'avoir assez d'articles à traiter
        titre = article.find('h3').text if article.find('h3') else "Titre non trouvé"
        lien = article.find('a', href=True)['href']
        lien_complet = f"https://news.google.com{lien[1:]}" if lien.startswith('.') else lien
        if lien_complet not in articles_deja_traites:  # Vérifier si l'article a déjà été traité
            resultats.append({'titre': titre, 'lien': lien_complet})
            articles_deja_traites.add(lien_complet)  # Marquer comme traité
        if len(resultats) == 10:  # Limiter à 10 articles nouveaux et uniques
            break
    return resultats, articles_deja_traites

def extraire_infos_article(url):
    try:
        reponse = requests.get(url, timeout=5)
        reponse.raise_for_status()
        soup = BeautifulSoup(reponse.content, 'html.parser')
        titre = soup.find('h1') or soup.find('title')
        titre = titre.text.strip() if titre else "Titre non trouvé"
        date = soup.find('time') or soup.find(lambda tag: 'date' in tag.attrs.get('class', '') or 'date' in tag.attrs.get('id', ''))
        date = date.text.strip() if date else "Date non trouvée"
        contenu = ' '.join(p.text for p in soup.findAll('p'))
        return {'titre': titre, 'date': date, 'contenu': contenu}
    except Exception as e:
        return None

# Exécution principale
entreprise = input("Entrez le nom de l'entreprise : ")
articles_deja_traites = set()
articles_valides = []

while len(articles_valides) < 10:
    articles, articles_deja_traites = rechercher_articles_google_news(entreprise, articles_deja_traites)
    for article in articles:
        infos = extraire_infos_article(article['lien'])
        if infos:  # Si l'extraction réussit
            articles_valides.append(infos)
            print(f"Titre: {infos['titre']}, Date: {infos['date']}, Contenu:\n{infos['contenu']}\n")
            if len(articles_valides) == 10:
                break
        # Si infos est None, cela signifie que l'extraction a échoué et l'article est ignoré
