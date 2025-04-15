import psycopg2 as psy
from datetime import date, datetime

connection = {
"dbname":       "pedraodb",
"user":         "postgres",
"password":     "2009",
"host":         "localhost",
"port":         "5432"
}

def addProduct(name, url, picturePath, price, coupon, category, phrase):
    try:
        with psy.connect(**connection) as conn:
            with conn.cursor() as cur:
                log(f"[TRY] ADD NEW IN products VALUES ({name}, {picturePath}, {coupon} {category}, {phrase})")
                query = f""" 
                    INSERT INTO products(name, url, picture_path, coupon, category, phrase) 
                    VALUES(%s, %s, %s, %s, %s, %s);
                """
                cur.execute(query, (name, url, picturePath, coupon, category, phrase))
                conn.commit()
                
                addPrice(price, url)

                log(f"ADDED NEW IN products/{getProductID(url)} VALUES ({name}, {picturePath}, {coupon} {category}, {phrase})")
            
    except psy.Error as e:
        log(f"DATABASE ERROR: {e}")
        return -1


()
def addPrice(price, iden):
    try: 
        with psy.connect(**connection) as conn:
            with conn.cursor() as cur:
                product_id = getProductID(iden)
                log(f"[TRY] ADD NEW IN product_price VALUES ({price}, {product_id})")
        
                query = f""" 
                    INSERT INTO product_price(price, date, product_id)
                        VALUES(%s, %s, %s);
                """
                cur.execute(query, (price, date.today(), product_id))
                conn.commit()

                query = f""" 
                    SELECT price_id
                        FROM product_price
                        NATURAL JOIN products
                        WHERE product_id = {product_id}
                        ORDER BY date DESC
                        LIMIT 1;
                """
                cur.execute(query)
                new_price_id = cur.fetchone()[0]

                log(f"ADDED NEW price IN product_price/{product_id}")
    except psy.Error as e:
        log(f"DATABASE ERROR: {e}")
        return -1

#identificador pode ser o id ou a url, detecta sozinho qual foi inserido
#sdds sobrecarga em java
def getProduct(iden, *columns):
    try:
        with psy.connect(**connection) as conn:
            with conn.cursor() as cur:

                formated_columns = ", ".join(columns)

                where_clause = {
                    str: f"WHERE url = '{iden}'",
                    int: f"WHERE product_id = {iden}"
                }

                query = f""" 
                            SELECT {formated_columns}
                                FROM product_price
                                NATURAL JOIN products
                                {where_clause[type(iden)]}
                                ORDER BY date DESC
                                LIMIT  1;
                            """
        
                cur.execute(query)
                product = cur.fetchone()

                logs = {
                    str: f"READ {formated_columns} FROM products/{getProductID(iden)}",
                    int: f"READ {formated_columns} FROM products/{iden}"
                }
                log(logs[type(iden)])

                return product
        
    except psy.Error as e:
        log(f"DATABASE ERROR: {e}")
        return -1

def getProductID(url):
    try:
        with psy.connect(**connection) as conn:
            with conn.cursor() as cur:
                query = f""" 
                    SELECT product_id 
                        FROM products
                        WHERE url = '{url}';
                        """
                cur.execute(query)
                productID = cur.fetchone()[0]

                log(f"READ id FROM products/{productID}")
                return productID

    except psy.Error as e:
        log(f"DATABASE ERROR: {e}")
        return -1
    except TypeError: 
        log(f"FAIL READ id FROM products/{url}: Not found")
        return -1

def log(msg):
    timestamp = datetime.now().strftime('[%d/%m/%Y::%H:%M:%S]')

    with open('/home/kaiqbbrs/pedraobot/main/logs/databaseLogs.log', "a") as log:
        log.write(f"{timestamp} {msg}\n")
