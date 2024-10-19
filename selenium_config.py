import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import logging

# Funzione per caricare il CSV
def load_csv(file_path):
    return pd.read_csv(file_path)

# Configurazione di Selenium WebDriver
def configure_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(service=Service('~/path/chromedriver'), options=chrome_options)
    driver.implicitly_wait(10)  # Timeout dinamico per caricamento pagine
    return driver

# Funzione per navigare su un sito e automatizzare alcune richieste
def automate_website(url):
    driver = configure_driver()
    try:
        driver.get(url)  # Visita l'URL
        print(f"Aperto {url}")
        
        # Attendi che la pagina sia completamente caricata (usando un approccio dinamico)
        time.sleep(1)
        
        # Esempio di automazione - cerca elementi della pagina
        links = driver.find_elements(By.TAG_NAME, "a")
        print(f"Trovati {len(links)} link su {url}")

    except Exception as e:
        logging.error(f"Errore durante l'apertura di {url}: {e}")
    finally:
        driver.quit()

# Funzione principale
def main():
    
    csv_file = "~/path/website_classification_100.csv"
    df = load_csv(csv_file)
    
    urls = df.iloc[:, 1].tolist()
    
    with ThreadPoolExecutor(max_workers=5) as executor:  
        futures = [executor.submit(automate_website, url) for url in urls]
        
        for future in as_completed(futures):
            try:
                future.result()
            except Exception as e:
                logging.error(f"Errore nell'esecuzione di una richiesta parallela: {e}")

if __name__ == "__main__":
    main()