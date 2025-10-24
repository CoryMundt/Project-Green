import sqlite3
from PGfunctions import readData,  from_dict, writeData, to_dict
from MarketDataTables import MarketDataTable
import subprocess
import sys
from pathlib import Path

### This file is for the user to create tables not inlcuded in default list:
### ["15min", "30min", "1hour", "6hour", "12hour", "1day", "7day", "14day", "30day", "60day", "90day"]
while True:
    run = input("Would you like to create a table not included by default? Y/N: ")
    if run.upper() not in ('Y', 'N'):
        continue
    else:
        if run.upper() == "N":
            quit()
        else:
            break

conn = sqlite3.connect('MarketData.sqlite')
cur = conn.cursor()
data = readData()

### Core code for this file, only a function to avoid duplicate big blocks of code to account for user creating multiple
### custom tables at one time
def createTables():
    global data
    ### Creates an individual table within the database given the following variables:
    ### acronym: the acronym for the crypto currency
    ### timeunit: hour, day, min
    ### denom: denomination of time unit e.g. 15 for 15 min if time unit is min
    ### cursor: cursor for communiticating to database
    def createCandleTable(acronym, timeunit, denom, cursor):
        global data
        if timeunit.lower() not in ("hour", "day", "min"):
            raise ValueError("Invalid value. Allowed values are min, hour, day")
        newDataTable = MarketDataTable(acronym, timeunit, denom)
        name = newDataTable.name
        ### to_dict converts MarketDataTable object to dict in order to store/save it within json file
        newDataTable = to_dict(newDataTable)
        key = str(denom) + timeunit
        data[acronym]["tables"][key] = newDataTable
        cursor.executescript(f'''
                              CREATE TABLE IF NOT EXISTS {name}(
                              Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                              Unix TEXT Unique,
                              Low DECIMAL(4, 6),
                              High DECIMAL(4, 6),
                              Open DECIMAL(4, 6),
                              Close DECIMAL(4, 6),
                              Volume INTEGER
                              );
                              ''')
    while True:
        acronym = input("Enter 3 letter acronym for the crypto you would like to add a table to, if you want to add this table to all cryptos press Enter: ")
        acronym = acronym.upper()
        if len(acronym) < 1:
            break
        if acronym not in data:
            print("Error: Crypto does not exist in database")
            continue
        break
    while True:
        timeunit = input("Enter timeunit for candles, Hour/Day: ")
        if timeunit.lower() not in ('hour', 'day'):
            print('Error: Invalid timeunit')
            continue
        else:
            break
    while True:
        denom = input("Enter how many hours or days a candle should be: ")
        try:
            denom = int(denom)
            if denom % 1 != 0:
                print("Error: Please enter a whole number")
                continue
            break
        except:
            print("Error: Please enter a whole number")
            continue
    key = str(denom) + timeunit
    ### Checks whether a table already exists by searching for it within the json files
    ### Returns 0 or -1 depending on whether or not table exists in order to break out of the while loop and to also not prompt the user
    ### if they want the same table created for other crypto if the custom table does not have valid inputs
    def checkCreate():
        try:
            from_dict(data[acronym]['tables'][key])
            print('Table already exists')
            return -1
        except NameError:
            createCandleTable(acronym, timeunit, denom, cur)
            return 0

    firstLoop = True
    if len(acronym) > 1:
        while True:
            if not firstLoop:
                acronym = input("Would you like to create this same table for another crypto? If so input acronym, if not, press Enter: ")
                acronym = acronym.upper()
                if len(acronym) < 1:
                    break
            if checkCreate() != 0:
                break
            print("Table Created")
            firstLoop = False
    else:
        print("Creating tables...")
        for acronym in data:
            checkCreate()

        print("Done")
def sortData():
    global data
    ### Assigns an int value for the str variable timeunit of each tabel and returns a tuple of said int alongside
    ### the denomination of said time unit so that the tables can easily be compared
    def sortKey(item):
        ### MDT = MarketDataTable object
        MDT = from_dict(item[1])
        timeunitPriority = {"min": 0, "hour": 1, "day": 2}
        return (timeunitPriority[MDT.timeunit], MDT.denomination)
    ### Sorts the dictionary data by timeunit and then denomination
    for crypto in data:
        sortedTables = dict(sorted(data[crypto]["tables"].items(), key=sortKey))
        data[crypto]["tables"] = sortedTables
    writeData()

createTables()

while True:
    user = input("Would you like to create another table? Y/N: ")
    if user.upper() == "Y":
        createTables()
    elif user.upper() == "N":
        break
    else:
        print("Enter Y or N")
        continue
### Sorts data with the additions created by user
sortData()

venv_python = Path(sys.executable)
subprocess.run([venv_python, "UpdateTables.py"])
conn.close()
