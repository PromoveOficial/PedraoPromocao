import psycopg2 as psy
from datetime import date, datetime

connection = {
    "dbname":       "pedraodb",
    "user":         "postgres",
    "password":     "2009",
    "host":         "localhost",
    "port":         "5432"
}

#CRUD - create read update delete
#só pra relebrar kkkk

def addProduct(name, url, picturePath, price, coupon, category, phrase):
    conn = psy.connect(**connection)
    cur = conn.cursor()
    
    query = f""" 
        INSERT INTO products(name, url, picture_path, coupon, category, phrase) 
            VALUES('{name}', '{url}', '{picturePath}', '{coupon}', '{category}', '{phrase}');
    """
    cur.execute(query)
    conn.commit()
    
    query = f""" 
        SELECT id 
            FROM products
            WHERE url = '{url}';
    """
    cur.execute(query)
    productID = cur.fetchone()[0]
    
    addPrice(price, productID)

    cur.close()
    conn.close()

    log = f" ADDED '{url}' IN "

    

def addPrice(price, productID):
    conn = psy.connect(**connection)
    cur = conn.cursor()

    query = f""" 
        INSERT INTO product_price(price, date, product_id)
            VALUES({price}, '{date.today()}', {productID})
    """
    cur.execute(query)
    conn.commit()

    cur.close()
    conn.close()

#identificador pode ser o id ou a url, detecta sozinho qual foi inserido
#sdds sobrecarga em java
def getProduct(iden, *columns):
    formated_columns = ""
    for column in columns:
        print(column)
        formated_columns += column + ", "

    formated_columns = formated_columns[0:-2]
    print(formated_columns)
    queryURL = f""" 
                SELECT {formated_columns}
                    FROM product_price
	                NATURAL JOIN products
	                WHERE url = '{iden}'
	                ORDER BY date DESC
	                LIMIT  1;
                """
    queryID = f""" 
                SELECT {formated_columns}
                    FROM product_price
	                NATURAL JOIN products
	                WHERE product_id = {iden} 
	                ORDER BY date DESC
	                LIMIT  1;
                """

    querys = {
        str: queryURL,
        int: queryID
    }

    conn = psy.connect(**connection)
    cur = conn.cursor()

    query = querys[type(iden)]
    cur.execute(query)
    product = cur.fetchone()

    cur.close()
    conn.close()
 
    log = f" READ '{formated_columns}' FROM products"
    writeLog(log)

    return product

def getProductID(url):
    conn = psy.connect(**connection)
    cur = conn.cursor()
    
    query = f""" 
        SELECT id 
            FROM products
            WHERE url = '{url}';
            """
    cur.execute(query)
    productID = cur.fetchone()[0]

    conn.close()
    cur.close()

    log = f" READ id FROM products/{productID}"
    writeLog(log)

    return productID

def writeLog(message):
    dateTime = datetime.now().strftime('[%d/%m/%Y::%H:%M:%S]')
    
    logsDirectoryPath = 'main/logs'

    logFile = open(logsDirectoryPath + '/databaseLogs.log', "a")
    logFile.write(dateTime + message + "\n")
    logFile.close()


#addProduct('nome', 'site.com', 'caminho/imagem', 320.44, 'CUPOM10', 'SpF10', 'Frase foda'
teste = getProduct(5, "name", "url", "picture_path", "price")
print(getProductID(teste[1]))
