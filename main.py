#!/usr/bin/env python3

from main.data import database as db
from main.administration import scrapper as scr


def main():
    action = input("Choose an action (1: Scrape Product, 2: Exit): ").strip()
    
    if action == '1':
        try:
            while True:
                print("Welcome to the Product Scraper!")
                url = input("Enter the product URL (or 'exit' to quit): ").strip()
                
                if url.lower() == 'exit':
                    print("Exiting the program.")
                    break
                
                product_info = scr.getProductInfo(url)
                
                if product_info:
                    print(f"Product Name: {product_info['name']}")
                    print(f"Product Price: {product_info['price']}")
                    print(f"Product Picture URL: {product_info['picture_url']}")
                    
                    # Save to database
                    db.addProduct(product_info['name'], url, product_info['price'], "nada", "nada", "nada")
                    print("Product information saved to the database.")
                else:
                    print("Failed to retrieve product information. Please check the URL and try again.")
                print("\n" + "="*40 + "\n")
        except KeyboardInterrupt as e:
            print("\nExiting...")
            print("Program terminated by user.")
        except Exception as e:
            print(f"An error occurred: {e}")

    elif action == '2':
        print("Exiting the program.")
        return 
    
if __name__ == "__main__":
    main()
