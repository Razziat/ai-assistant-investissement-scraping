from pygooglenews import GoogleNews
from datetime import datetime
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from requests_html import HTMLSession
from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
import time
import os
import requests

def get_article_content(url):
    try:
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')

        # Utilisez ChromeService avec ChromeDriverManager
        service = ChromeService(executable_path=ChromeDriverManager().install())

        # Créez l'instance du WebDriver avec le service spécifié
        driver = webdriver.Chrome(service=service, options=options)

        driver.get(url)
        print("URL actuelle:", driver.current_url)
        try:
            # Attendre que le bouton d'acceptation des cookies soit visible et cliquer dessus
            accept_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "/html/body/c-wiz/div/div/div/div[2]/div[1]/div[3]/div[1]/div[1]/form[2]/div/div/button/span"))
            )
            accept_button.click()
            # Attendre un moment pour que la page se recharge après l'acceptation
            time.sleep(3)
        except TimeoutException:
            print("Bouton d'acceptation des cookies non trouvé, continuation.")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.TAG_NAME, "p")))
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        paragraphs = soup.find_all('p')
        if not paragraphs:
            driver.quit()
            return "No article content found or dynamically loaded."

        article_text = ' '.join(p.get_text() for p in paragraphs)
        driver.quit()
        return article_text
    except Exception as e:
        print(f"General Error: {type(e).__name__}, {e}")
        if driver is not None:
            driver.quit()
        return "Failed to retrieve the article."

def get_articles(keyword, start_date, end_date):
    gn = GoogleNews()
    start = datetime.strptime(start_date, '%m/%d/%Y').strftime('%Y-%m-%d')
    end = datetime.strptime(end_date, '%m/%d/%Y').strftime('%Y-%m-%d')

    search = gn.search(keyword, from_=start, to_=end)
    articles_list = []

    for entry in search['entries']:
        article_content = get_article_content(entry.link)
        articles_list.append({
            'Title': entry.title,
            'Published': entry.published,
            'Link': entry.link,
            'Content': article_content
        })

    df = pd.DataFrame(articles_list)
    return df

if __name__ == "__main__":
    keyword = input("Entrez le mot-clé pour la recherche d'articles : ")
    start_date = input("Entrez la date de début (mm/jj/aaaa) : ")
    end_date = input("Entrez la date de fin (mm/jj/aaaa) : ")

    articles_df = get_articles(keyword, start_date, end_date)
    print(articles_df)

    dossier_cible = f"datas/{keyword.replace(' ', '_')}_{start_date.replace('/', '-')}_{end_date.replace('/', '-')}"
    chemin_complet = os.path.join(dossier_cible, f"{keyword.replace(' ', '_')}_articles.csv")

    # Vérifier si le dossier existe, sinon le créer
    if not os.path.exists(dossier_cible):
        os.makedirs(dossier_cible)

    # Sauvegarder le fichier CSV
    articles_df.to_csv(chemin_complet, index=False)

    print(f"Fichier CSV sauvegardé à : {chemin_complet}")
