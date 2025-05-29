#!/usr/bin/env python3

from main.data import database as db
from main.administration import scrapper as scr


def main():
    try:
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
    except KeyboardInterrupt as e:
        print("\nExiting...")
        print("Program terminated by user.")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
