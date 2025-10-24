import os
from dotenv import find_dotenv, load_dotenv
import coinbase
from coinbase.rest import RESTClient
import sqlite3
from PGfunctions import createDefaultCandleTables,  readData, writeData
import time
from datetime import datetime
import subprocess
import sys
from pathlib import Path

while True:
    run = input("Would you like to create a new crypto in database? Y/N: ")
    if run.upper() not in ('Y', 'N'):
        continue
    else:
        if run == "N":
            quit()
        else:
            break
### Creates a connection to the database and then a cursor with which we can run sql to modify the database
### If the database does not exist yet, it creates an empty one
conn = sqlite3.connect('MarketData.sqlite')
cur = conn.cursor()

### This is fetching api keys from the .env file. Currently read-only keys for one of my accounts.
### Each instance of the program, if this program was to actually be used by other people, would have unique api
### keys, and we obviously we don't want those api keys within the code itself

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

api_key = os.getenv("api_key")
secret_key = os.getenv("api_secret")
client = RESTClient(api_key=api_key, api_secret=secret_key, timeout=5)

data = readData()
firstLoop = True
while True:
    if not firstLoop:
        run = input("Would you like to create another crypto in database? Y/N: ")
        if run.upper() not in ('Y', 'N'):
            continue
        else:
            if run.upper() == "N":
                break
    while True:
        acronym = input('Enter 3 letter Crypto acronym or leave empty and press enter to quit: ')
        acronym = acronym.upper()
        if len(acronym) < 1:
            quit()
        if len(acronym) != 3:
            print("Error: Invalid Acronym")
            continue
        ### Checks whether entered crypro acronym already exists in the database to avoid duplicates
        if acronym not in data:
            new_crypto = {
                "gotData": False,
                "prevStart": "",
                "tables": createDefaultCandleTables(acronym, cur)
            }
            data[acronym] = new_crypto
        else:
            print("Error: Crypto already Exists")
            continue
        ### Gets the datetime of now and converts that to a unix timestamp, then subtracts a day's worth of seconds
        ### to get start unix timestamp for the test below
        end = str(int(time.mktime(datetime.now().timetuple())))
        start = str(int(end) - 90000)
        try:
            ### get_candles(client, crypto_market, str(int(unixtimestamp)), str(int(unixtimestamp)), per candle time period)
            ### Checks whether the inputs are valid, before adding anything to the data base by issuing a small query to the api
            MarketData = coinbase.rest.RESTClient.get_candles(client, acronym + "-USD", start, end, "ONE_DAY")
            writeData()
            firstLoop = False
            break
        except Exception as e:
            print(e)
            del data[acronym]

venv_python = Path(sys.executable)
subprocess.run([venv_python, "UpdateTables.py"])
conn.close()
