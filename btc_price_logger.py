# Bitcoin Price Logger
# Author: Zach Gillis

import requests
import mysql.connector
import time
import datetime
from config import db

# API URL for Bitcoin price
URL = "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"
price = None

# Attempt to request Bitcoin price
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


# Attempt to save in MySQL database
try:
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    print("Connecting to database at %s..." % (db['host']))

    db = mysql.connector.connect(host=db['host'], user=db['user'], passwd=db['passwd'], database=db['db_stats'])
    cursor = db.cursor()

    sql = """INSERT INTO LOGGING(LI_ID, LOG_TMST, LOG_VALUE) VALUES(%s, %s, %s)"""
    values = (1, timestamp, price)

    print("Inserting price log record...")

    cursor.execute(sql, values)
    db.commit()

    print("Price log stored successfully. Exiting.")

except:
    print("Failed to store BTC price in database.")



