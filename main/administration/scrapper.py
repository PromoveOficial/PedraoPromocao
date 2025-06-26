#!/home/kaiqbbrs/promove/pedraobot/.venv/bin/python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wwait
from selenium.webdriver.support import expected_conditions as EC    

# Carrega as variáveis de ambiente do arquivo .env
from dotenv import load_dotenv
from logging import Logger
import logging  

load_dotenv()

def getProductInfo(logger: Logger, url):
    # logger.debug(f"[TRY: READ PRODUCT] {url}")    

    site = url.split('/')[2]
    logger.debug(site)
    
    product = {}
    
    try:
        if site in ['www.amazon.com.br', 'amzn.to']:
            product = amazon(url, product)
        elif site in ['www.mercadolivre.com.br', 'produto.mercadolivre.com.br', 'mercadolivre.com']:
            product = mercadoLivre(logger, url, product)
        elif site == 'www.netshoes.com.br':
            product = netshoes(url, product)
        else: 
            product = "Site not supported."
    except Exception as e:
        logger.critical(e)
        product = None

    # logger.debug(f"[SUCCEDED: READ PRODUCT] {url}") 
    return product


def amazon(url, product):
    driver = webdriver.Chrome()
    driver.get(url)
        
    """ Espera carregar e pega o nome"""
    product['name'] = wwait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'productTitle'))
    ).text

    """ Pega o preço e formata """
    price_div = driver.find_element(By.CLASS_NAME, 'a-price')
    price_string = (price_div
                    .find_element(By.XPATH, './*[2]')
                    .text
                    .replace('\n', ',')    #para deixar em um formato melhor para ser tratada 
                    )                      #posteriormente
    
    product['price'] = price_string[2:]

    """ Pega a url para baixar a imagem """
    picture_element = driver.find_element(By.ID, 'landingImage')
    product['picture_url'] = picture_element.get_attribute('src')
    

    driver.quit()
    return product

def netshoes(url, product):
    driver = webdriver.Chrome()
    driver.get(url)
   
    """ Espera carregar e pega o nome"""
    product['name'] = wwait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'product-name'))
    ).text
    
    """ Pega o preço e formata """
    product['price'] = (driver.find_element(By.CSS_SELECTOR, 'span.saleInCents-value')
                        .get_attribute('outerHTML')
                        .split(' ')[15][:-1])

    """ Pega a url para baixar a imagem """
    product['picture_url'] = (driver
                              .find_element(By.CLASS_NAME, 'carousel-item-figure__image')
                              .get_attribute('src'))

    driver.quit()
    return product


def mercadoLivre(logger, url, product):
    driver = webdriver.Chrome()
    
    if url.split('/')[3] == 'sec':
        driver.get(url)
        url = wwait(driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'a.poly-component_link.poly-component_link--action-link'))
        ).get_attribute('href')
        logger.debug(url)
    
    driver.get(url)
    
    """ Espera o site carregar e pega o nome do produto """
    product['name'] = wwait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'ui-pdp-title'))
    ).text
   
    """ Pega o preço """
    price_element = driver.find_element(By.CSS_SELECTOR, 'meta[itemprop="price"]') 
    price_text = price_element.get_attribute('content')
    product['price'] = price_text
    
    """ Pega o url para baixar a imagem """
    picture_element = driver.find_element(By.CLASS_NAME, 'ui-pdp-gallery__figure__image')
    product['picture_url'] = picture_element.get_attribute('src')
    
    driver.quit()
    return product


def __main__():
    logger = logging.getLogger(__name__)
    
    if not logger.hasHandlers():
            logger.setLevel(logging.DEBUG)

            handler = logging.StreamHandler()

            formatter = logging.Formatter(
                # '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                '[%(asctime)s] [%(levelname)s] %(message)s'
            )

            handler.setFormatter(formatter)
            logger.addHandler(handler)
    
    try:
        while True:
            url = input('url:\n')
            logger.debug(getProductInfo(logger, url))
    except KeyboardInterrupt:
        logger.debug('Exiting...')
        
if __name__ == '__main__':
    __main__()