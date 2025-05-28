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

    def getTextMessageBody(self):
        f"""Produto: {self.name}, Preço: {self.price}, e tudo mais q tem q ter, aguarde o chefinho mandar
        """

    def categorize(self):
        if category != "":
            return

        #Em processo de pensar

    def verifyImage(self):
        arquivos = glob.glob(f"pictures/{self.id}.*") 
        if arquivos:
            return 1
