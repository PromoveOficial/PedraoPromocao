#!/usr/bin/env python3

from data import database as db
from services import scrapper as scr
import re


def main():
    #try:
        while True:

            url = input("url: \n")
            
            #Vou deixar os 3 vazios para testar por enquanto, esses tem q ser inseridos manualmente
            coupon = ""
            category = ""
            phrase = ""
            #
            
            product_info = scr.getProductInfo(url)

            name = product_info['name']
            price = product_info['price']
            
            if db.addProduct(name, url, price, coupon, category, phrase) == 1:
                p_id = db.getProductID(url)
                db.updateProduct(p_id, coupon="TESTEFODA", category="teste categoria")
                print(db.getProduct(p_id, "*"))
    #except Exception as e:
    #    print(e)

if __name__ == "__main__":
    main()
