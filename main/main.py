#!/usr/bin/env python3

from data import database as db
from services import scrapper as scr



def main():
    url = input()
    
    #Vou deixar os 3 vazios para testar por enquanto, esses tem q ser inseridos manualmente
    coupon = ""
    category = ""
    phrase = ""
    #
    
    product_info = scr.getProductInfo(url)

    name = product_info['name']
    price = product_info['price']
    
    print(name, price)

    #if db.addProduct(name, url, price, coupon, category, phrase) == 1:
    #   print(db.getProduct(url, "name", "picture_path", "price"))
    


if __name__ == "__main__":
    main()
