import sqlite3
from PGfunctions import readData, from_dict, writeData

### This file is for users to delete individual tables they do not want except for 15min, 1 hour, and 1 day
### as those 3 tables are required for the program to work
while True:
    run = input("Would you like to delete a table Y/N: ")
    if run.upper() not in ('Y', 'N'):
        continue
    else:
        if run == "N":
            quit()
        else:
            break
conn = sqlite3.connect('MarketData.sqlite')
cur = conn.cursor()
data = readData()

### Prompts user for crypto they want to delete a specific table from or has them press enter
### to delete from all cyrptos. It then walks them through a series of prompts to get the specific
### table they want to delete
def deleteTables():
    global data
    while True:
        acronym = input("Enter 3 letter acronym for the crypto you would like to delete a table from, if you want to delete this table from all cryptos press Enter: ")
        acronym = acronym.upper()
        if len(acronym) < 1:
            break
        if acronym not in data:
            print("Error: Crypto does not exist in Database")
            continue
        break

    while True:
        denom = input("Enter how many hours or days a candle is: ")
        try:
            denom = int(denom)
            if denom % 1 != 0:
                print("Error: Please enter a whole number")
                continue
            if denom <= 1:
                print("Error: Please enter a whole number greater than 1")
                continue
            break
        except:
            print("Error: Please enter a whole number")
            continue

    while True:
        timeunit = input("Enter timeunit for candles, Hour/Day: ")
        if timeunit.lower() not in ('hour', 'day'):
            print('Error: Invalid timeunit')
        else:
            break

    key = str(denom) + timeunit

    ### Checks to see if the table exists json file in order to delete it, if it does, it deltes it, 
    ### if not, nothing happens
    def checkDelete():
        global data
        try:
            table = from_dict(data[acronym]['tables'][key])
            cur.execute(f'DROP TABLE IF EXISTS {table.name}')
            del data[acronym]['tables'][key]
            conn.commit()
            return 0
        except:
            return -1

    firstLoop = True

    if len(acronym) > 1:
        while True:
            if not firstLoop:
                acronym = input("Would your like to delete this table for another crypto? If so input acronym, if not, press Enter: ")
                acronym = acronym.upper()
                if len(acronym) < 1:
                    break
            if checkDelete() != 0:
                break
            print("Table Deleted")
            firstLoop = False
    else:
        print("Deleting tables...")
        for acronym in data:
            checkDelete()
        print("Tables deleted")

deleteTables()

while True:
    user = input("Would you like to delete another table? Y/N: ")
    if user.upper() == "Y":
        deleteTables()
    elif user.upper() == "N":
        writeData()
        conn.close()
        print("Done")
        quit()
    else:
        print("Enter Y or N")
        continue
