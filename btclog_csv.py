# Bitcoin Price Logger
# Author: Zach Gillis

import requests
import time
import datetime
import csv

# API URL for Bitcoin price
URL = "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"

while True:
    price = None

    try:
        print("Requesting BTC/USD price...")
        r = requests.get(URL)
        data = r.json()

        price = data['bpi']['USD']['rate']
        price = float(price.replace(',', ''))
        print("Price retrieved ($" + str(price) + " USD/1 BTC)")

    except Exception as e:
        print("Failed to retrieve BTC price.")
        print(e)
        exit(5)

    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')

    values = (1, timestamp, price)

    row = [timestamp, price]
    with open('btclog.csv', 'a') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)
    csvFile.close()

    print("Price log stored successfully.")

    time.sleep(30)
