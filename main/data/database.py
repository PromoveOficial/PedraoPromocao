import psycopg2 as psy
from datetime import date
import os

from ..utils import log
# Carrega as variáveis de ambiente do arquivo .env
from dotenv import load_dotenv
load_dotenv()

# Define origem dinâmica para os logs
ENV_STATE = os.getenv("DEBUG")
LOG_ORIGIN = f"DATABASE"

CONNECTION = {
    "dbname":       "pedraodb",
    "user":         "postgres",
    "password":     "2009",
    "host":         "localhost",
    "port":         "5432"
}

def addProduct(name, url, price, coupon, category, phrase):
    log(LOG_ORIGIN, f"[TRY: ADD PRODUCT] product/{url}")
    try:
        with psy.connect(**CONNECTION) as conn:
            with conn.cursor() as cur:
                query = """
                    INSERT INTO products(name, url, coupon, category, phrase)
                    VALUES(%s, %s, %s, %s, %s);
                """
                cur.execute(query, (name, url, coupon, category, phrase))
                conn.commit()
                addPrice(price, url)
                product_id = getProductID(url)
                log(LOG_ORIGIN, f"[SUCCEDED: ADD PRODUCT] product/{product_id}")
                return 1
    except psy.Error as e:
        log(LOG_ORIGIN, f"[FAILED: ADD PRODUCT] product/{url} - {e}")
        return -1

def addPrice(price, iden):
    log(LOG_ORIGIN, f"[TRY: ADD PRICE] product/{iden}")
    try:
        with psy.connect(**CONNECTION) as conn:
            with conn.cursor() as cur:
                product_id = getProductID(iden)
                query = """
                    INSERT INTO product_price(price, date, product_id)
                    VALUES(%s, %s, %s);
                """
                cur.execute(query, (price, date.today().strftime("%d/%m/%Y"), product_id))
                conn.commit()
                query = """
                    SELECT price_id
                    FROM product_price
                    NATURAL JOIN products
                    WHERE product_id = %s
                    ORDER BY date DESC
                    LIMIT 1;
                """
                cur.execute(query, (product_id,))
                new_price_id = cur.fetchone()[0]
                log(LOG_ORIGIN, f"[SUCCEDED: ADD PRICE] product_price/{new_price_id}")
                return 1
    except psy.Error as e:
        log(LOG_ORIGIN, f"[FAILED: ADD PRICE] product/{iden} - {e}")
        return -1

def getProduct(iden, *columns):
    columns_str = ", ".join(columns) if columns else "*"
    log(LOG_ORIGIN, f"[TRY: READ PRODUCT] products/{iden}")
    try:
        with psy.connect(**CONNECTION) as conn:
            with conn.cursor() as cur:
                where_clause = {
                    str: f"WHERE url = '{iden}'",
                    int: f"WHERE product_id = {iden}"
                }
                query = f"""
                    SELECT {columns_str}
                    FROM product_price
                    NATURAL JOIN products
                    {where_clause[type(iden)]}
                    ORDER BY date DESC
                    LIMIT 1;
                """
                cur.execute(query)
                product = cur.fetchone()
                affected = f"products/{getProductID(iden)}" if isinstance(iden, str) else f"products/{iden}"
                log(LOG_ORIGIN, f"[SUCCEDED: READ PRODUCT] {affected}")
                return product
    except psy.Error as e:
        log(LOG_ORIGIN, f"[FAILED: READ PRODUCT] products/{iden} - {e}")
        return -1

def getProductID(url):
    log(LOG_ORIGIN, f"[TRY: READ PRODUCT ID] products/{url}")
    try:
        with psy.connect(**CONNECTION) as conn:
            with conn.cursor() as cur:
                query = """
                    SELECT product_id
                    FROM products
                    WHERE url = %s;
                """
                cur.execute(query, (url,))
                productID = cur.fetchone()[0]
                log(LOG_ORIGIN, f"[SUCCEDED: READ PRODUCT ID] product/{productID}")
                return productID
    except psy.Error as e:
        log(LOG_ORIGIN, f"[FAILED: READ PRODUCT ID] products/{url} - {e}")
        return -1
    except TypeError:
        log(LOG_ORIGIN, f"[FAILED: READ PRODUCT ID] products/{url} - Not found")
        return -1

def updateProduct(iden, name=None, url=None, picturePath=None, price=None, coupon=None, category=None, phrase=None):
    log(LOG_ORIGIN, f"[TRY: UPDATE PRODUCT] products/{iden}")
    try:
        product_id = getProductID(iden if isinstance(iden, str) else None) if isinstance(iden, str) else iden
        if product_id == -1:
            log(LOG_ORIGIN, f"[FAILED: UPDATE PRODUCT] products/{iden} - Product not found")
            return -1

        updates = []
        values = []

        if name is not None:
            updates.append("name = %s")
            values.append(name)
        if url is not None:
            updates.append("url = %s")
            values.append(url)
        if picturePath is not None:
            updates.append("picture_path = %s")
            values.append(picturePath)
        if coupon is not None:
            updates.append("coupon = %s")
            values.append(coupon)
        if category is not None:
            updates.append("category = %s")
            values.append(category)
        if phrase is not None:
            updates.append("phrase = %s")
            values.append(phrase)

        if updates:
            with psy.connect(**CONNECTION) as conn:
                with conn.cursor() as cur:
                    set_clause = ", ".join(updates)
                    query = f"""
                        UPDATE products
                        SET {set_clause}
                        WHERE product_id = %s;
                    """
                    values.append(product_id)
                    cur.execute(query, tuple(values))
                    conn.commit()
                    log(LOG_ORIGIN, f"[SUCCEDED: UPDATE PRODUCT] products/{product_id}")

        # Adiciona novo preço, sem sobrescrever os antigos
        if price is not None:
            addPrice(price, product_id)
        return 1

    except psy.Error as e:
        log(LOG_ORIGIN, f"[FAILED: UPDATE PRODUCT] products/{iden} - {e}")
        return -1