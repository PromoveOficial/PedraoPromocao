from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wwait
from selenium.webdriver.support import expected_conditions as EC

import sys
import os
sys.path.append(os.path.abspath('..')) #Para incluir os modulos em main/      

from utils import log

def getProductInfo(url):
    log("scrapper",  f'[TRY: READ PRODUCT FROM "{url}"]')    
    
    product = {
        'name': '',
        'price': '',
        'picture_url': ''
    }

    site = url.split('/')[2].split('.')[1]
    
    try:
        if site == 'amazon':
            product = amazon(url, product)
        elif site == 'mercadolivre':
            product = mercadoLivre(url, product)
        elif site == 'netshoes':
            product = netshoes(url, product)
        else: 
            log("scrapper",  f'[ERROR: READING PRODUCT FROM "{url}"] ERROR: Site not supported')
    except Exception as e:
        log("scrapper", f'[ERROR: READING PRODUCT FROM "{url}"] ERROR: {e}')

    log("scrapper",  f'READ "{url}"') 
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


def mercadoLivre(url, product):
    driver = webdriver.Chrome()
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
