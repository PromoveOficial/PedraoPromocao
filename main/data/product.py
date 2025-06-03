import os
import glob

class Product:
    def __init__(self, id, name, url, price, coupon , category, phrase):
        self.name = ""
        self.url = ""
        self.price = ""
        self.coupon = ""
        self.category = ""
        self.phrase = ""

    def basicMessage(self):
        mensagem = """"""
        
    def verifyImage(self):
        arquivos = glob.glob(f"pictures/{self.id}.*") 
        if arquivos:
            return 1
        
        
