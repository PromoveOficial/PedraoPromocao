from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait as wwait
from selenium.webdriver.support import expected_conditions as EC

import sys
import os
sys.path.append(os.path.abspath('..')) #Para incluir os modulos em main/      

from libs import utils

def getProductInfo(url):
    utils.write_log("scrapper",  f'[TRY] READ "{url}"')    
    
    product = {
        'name': '',
        'price': '',
        'picture_url': ''
    }

    site = url.split('/')[2].split('.')[1]
   
    if site == 'amazon':
        product = amazon(url, product)
    elif site == 'mercadolivre':
        product = mercadoLivre(url, product)
    elif site == 'netshoes':
        product = netshoes(url, product)
    else: 
        utils.write_log("scrapper",  f'ERROR READING "{url}": Site not supported')
   
    if product == 0:
        utils.write_log("scrapper",  f'FAIL READ "{url}"')
        return 0
    

    utils.write_log("scrapper",  f'READ "{url}"') 
    return product


def amazon(url, product):
    try:
        driver = webdriver.Chrome()
        driver.get(url)
        
        product['name'] = wwait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, 'productTitle'))
        ).text


        price_div = driver.find_element(By.CLASS_NAME, 'a-price')
        price_string = (price_div
                        .find_element(By.XPATH, './*[2]')
                        .text
                        .replace('\n', ',')    #para deixar em um formato melhor para ser tratada 
                        )                      #posteriormente
        
        product['price'] = price_string[2:]

        picture_element = driver.find_element(By.ID, 'landingImage')
        product['picture_url'] = picture_element.get_attribute('src')
        

        driver.quit()
        return product

    except Exception as e:
        utils.write_log("scrapper",  f'ERROR: {e}')
        driver.quit()
        return 0


def netshoes(url, product):
    try:
        driver = webdriver.Chrome()
        driver.get(url)
       
        product['name'] = wwait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'product-name'))
        ).text
        
        product['price'] = (driver.find_element(By.CSS_SELECTOR, 'span.saleInCents-value')
                            .get_attribute('outerHTML')
                            .split(' ')[15][:-1])

        product['picture_url'] = (driver
                                  .find_element(By.CLASS_NAME, 'carousel-item-figure__image')
                                  .get_attribute('src')
                                  )

        driver.quit()
        return product

    except Exception as e:
        utils.write_log("scrapper",  f'ERROR: {e}')
        driver.quit()
        return 0


def mercadoLivre(url, product):
    try:
        driver = webdriver.Chrome()
        driver.get(url)
        
        """ Espera o site carregar e pega o nome do produto """
        product['name'] = wwait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'ui-pdp-title'))
        ).text
       
        """ Pega o preço e converte em float """
        price_element = driver.find_element(By.CSS_SELECTOR, 'meta[itemprop="price"]') 
        price_text = price_element.get_attribute('content')
        product['price'] = price_text
        
        """ Pega o url para baixar a imagem """
        picture_element = driver.find_element(By.CLASS_NAME, 'ui-pdp-gallery__figure__image')
        product['picture_url'] = picture_element.get_attribute('src')
        
        driver.quit()
        return product

    except Exception as e:
        utils.write_log("scrapper",  f'ERROR: {e}')
        driver.quit()
        return 0
