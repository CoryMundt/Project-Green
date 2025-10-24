import sqlite3
from PGfunctions import readData, from_dict, writeData
### This file is to delete all tables associated with a specified asset instead of manually deleting each one
while True:
    run = input("Would you like to delete a crypto Y/N: ")
    if run.upper() not in ('Y', 'N'):
        continue
    elif run == "N":
        quit()
    else:
        break

conn = sqlite3.connect('MarketData.sqlite')
cur = conn.cursor()
data = readData()
### Prompts user for crypto acronym to delete and then checks if the acronym is stored in the database by searching
### for it within the json file that keeps track of all cryptos and tables associated within them and then
### loops through drop table SQL queries to delete all tables associated with that crypto before deleting the
### crytpo from dictionary itself.
def deleteCrypto():
    while True:
        ### Ensures user inputs an asset that exists within the database
        acronym = input("Enter 3 letter acronym for the crypto to delete: ")
        acronym = acronym.upper()
        if len(acronym) < 1:
            continue
        if acronym not in data:
            print("Error: Crypto does not exist in Database")
            continue
        break
    while True:
        run = input(f"Are you sure you want to delete {acronym} Y/N: ")
        if run.upper() not in ('Y', 'N'):
            continue
        elif run == "N":
            quit()
        else:
            break
    tables = data[acronym]['tables']
    for table in tables.values():
        table = from_dict(table)
        cur.execute(f'DROP TABLE IF EXISTS {table.name}')
    del data[acronym]
    writeData()


deleteCrypto()

while True:
    user = input("Would you like to delete another crypto? Y/N: ")
    if user.upper() == "Y":
        deleteCrypto()
    elif user.upper() == "N":
        conn.close()
        print("Done")
        quit()
    else:
        print("Enter Y or N")
        continue
