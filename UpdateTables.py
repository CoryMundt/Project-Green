import os
from dotenv import find_dotenv, load_dotenv
from coinbase.rest import RESTClient
import sqlite3
from PGfunctions import update15minCandles, readData, updateOtherTable, from_dict, to_dict, readConfig, writeConfig

### This file updates all tables in the database, it runs the momment the user opens the program main.py because
### in the event the program is interrupted on the previous run, the previous run needs to finish before the user makes
### any changes to the database
conn = sqlite3.connect('MarketData.sqlite')
cur = conn.cursor()
dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

api_key = os.getenv("api_key")
secret_key = os.getenv("api_secret")
client = RESTClient(api_key=api_key, api_secret=secret_key, timeout=5)

data = readData()
config = readConfig()
### Checkpoint is the last completed/updated table saved in config.json in case program is interrupted, it is used as
### a reference on where to resume
checkpoint = config['checkpoint']
runs = config['runs']


try:
    resume = False
    ### When checkpoint is null/None means the last run completed or program has never run before
    if checkpoint is None:
        resume = True
    for crypto in data:
        ### See Sdata.json file for dict format, run program once if you do not see it
        try:
            tables = data[crypto]['tables']
        except:
            quit()
        for key, table in tables.items():
            table = from_dict(table)
            if not resume:
                if table != checkpoint:
                    continue
                else:
                    resume = True
                    continue
            else:
                ### These are the first tables of their respected timeunits and therefore are special cases
                match key:
                    case "15min":
                        update15minCandles(crypto, client, cur, conn)
                        checkpoint = to_dict(table)
                        continue
                    case "1hour":
                        sourceTable = from_dict(data[crypto]['tables']['30min'])
                        updateOtherTable(crypto, sourceTable.name, table.name, cur, conn)
                        checkpoint = to_dict(table)
                        continue
                    case "1day":
                        sourceTable = from_dict(data[crypto]['tables']['12hour'])
                        updateOtherTable(crypto, sourceTable.name, table.name, cur, conn)
                        checkpoint = to_dict(table)
                        continue
                    case _:
                        ### Looks for most efficient source table starting at the end of the dict, that has the same time unit and
                        ### the table with the least rows, and therefore the table that requires the least compuations,
                        ### to convert data
                        for item_key, item in reversed(tables.items()):
                            item = from_dict(item)
                            if item.timeunit == table.timeunit:
                                if table.denomination % item.denomination == 0:
                                    ### Ensures table's source table is not itself
                                    if table.denomination / item.denomination > 1:
                                        sourceTable = item
                                        ### iRows is the number of candles being condensed from source table into
                                        ### current one. e.g. Using 15 min as source table, and 30 min as the current
                                        ### table, Irows is set to 2
                                        iRows = table.denomination / sourceTable.denomination
                                        updateOtherTable(crypto, sourceTable.name, table.name, cur, conn, iRows)
                                        checkpoint = to_dict(table)
                                        break
    checkpoint = None
except KeyboardInterrupt:
    print("Error: Program interrupted by user")
except Exception as e:
    print(e)
finally:
    config['checkpoint'] = checkpoint
    if checkpoint is None:
        config['runs'] += 1
    writeConfig()

print('Done')
conn.close()
