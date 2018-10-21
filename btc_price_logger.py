# Bitcoin Price Logger
# Author: Zach Gillis

import requests
import mysql.connector
import time
import datetime
from config import db
from config import interval

# API URL for Bitcoin price
URL = "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"
sql = """INSERT INTO LOGGING(LI_ID, LOG_TMST, LOG_VALUE) VALUES(%s, %s, %s)"""

print("Connecting to database at %s..." % (db['host']))
dbcon = mysql.connector.connect(host=db['host'], user=db['user'], passwd=db['passwd'], database=db['db_stats'])
cursor = dbcon.cursor()

while True:
    price = None

    try:
        print("Requesting BTC/USD price...")
        r = requests.get(URL)
        data = r.json()

        price = data['bpi']['USD']['rate']
        price = float(price.replace(',', ''))
        print("Price retrieved ($" + str(price) + " USD/1 BTC)")

    except:
        print("Failed to retrieve BTC price.")
        exit(5)

    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    values = (1, timestamp, price)

    print("Inserting price log record...")

    cursor.execute(sql, values)
    dbcon.commit()
    print("Price log stored successfully.")

    time.sleep(interval)


