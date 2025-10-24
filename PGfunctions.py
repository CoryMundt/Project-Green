import coinbase
from coinbase.rest import RESTClient
import json
from MarketDataTables import MarketDataTable
import time
import re
from datetime import datetime
#import pytz

### Reads the Sdata.json file which is a dictionary of all the cryptos and their respective tables
def readData():
    global data
    try:
        ### This will only fail if json file does not exist or has been removed from the directory by the user
        ### in which case it creates a new blank one
        with open('Sdata.json', 'r') as file:
            data = json.load(file)
        return data
    except:
        with open('Sdata.json', 'w') as file:
            json.dump({}, file, indent=4)
        with open('Sdata.json', 'r') as file:
            data = json.load(file)
        return data
### Updates Sdata.json
def writeData():
    global data
    with open('Sdata.json', 'w') as file:
        json.dump(data, file, indent=4)

### This function reads the config.json file which keeps track of user's instance of the program between uses
def readConfig():
    global config
    try:
        ### Will only fail first run when json file is empty
        with open('config.json', 'r') as file:
            config = json.load(file)
        return config
    except:
        with open('config.json', 'w') as file:
            json.dump({"checkpoint": None, "lastStartDate": "",  "runs": -1, "backupRun": 50}, file, indent=4)
        with open('config.json', 'r') as file:
            config = json.load(file)
    return config

### Updates Config.json file
def writeConfig():
    global config
    with open('config.json', 'w') as file:
        json.dump(config, file, indent=4)

'''def get30past():
    dtime = datetime.now()
    Unix_TDPtime = time.mktime(dtime.timetuple()) - 2592000
    TDPtime = datetime.fromtimestamp(Unix_TDPtime)
    print("Date and Time Defaulted to : " + str(TDPtime))
    return TDPtime'''

'''def getmidnight():
    dnow = datetime.now()
    dtime = datetime(dnow.year, dnow.month, dnow.day, 0,0,0)
    Unix_TDPtime = time.mktime(dtime.timetuple())
    TDPtime = datetime.fromtimestamp(Unix_TDPtime)
    print("Date and Time Defaulted to : " + str(TDPtime))
    return TDPtime'''

### Used to get rid of // ,, ... in dates entered by user
def getnumbers(userinput):
    return re.sub("[^0-9^.]", "", userinput)

### Gets rid of leading 0 when inputting dates
def checkfrontzero(timevar):
    if timevar.startswith("0"):
        timevar = int(timevar[1])
    else:
        timevar = int(timevar)
    return timevar
### Ignore
'''def getdatetimerange(acronym):
    zerodate = datetime(2009, 1, 3)
    noneentered = False
    while True:
        while True:
            # Get Start Date
            try:
                Sinputdate = input("Enter Start date as MM-DD-YYYY, or press Enter to default the starting time to 30 days prior from now: ")
                if len(Sinputdate) < 1:
                    Sdatetime = get30past()
                    Sdate = datetime(Sdatetime.year, Sdatetime.month, Sdatetime.day)
                    noneentered = True
                    break
                elif Sinputdate == '/':
                    Sdatetime = getmidnight()
                    Sdate = datetime(Sdatetime.year, Sdatetime.month, Sdatetime.day)
                    noneentered = True
                    break
                else:
                    Sinputdate = getnumbers(Sinputdate)
                    Syear = int(Sinputdate[4:])
                    Smonth = Sinputdate[0:2]
                    Sday = Sinputdate[2:4]
                    Smonth = checkfrontzero(Smonth)
                    Sday = checkfrontzero(Sday)
                    Sdate = datetime(Syear, Smonth, Sday)
                    if Sdate < zerodate:
                        print("Error: Date Entered must be later than 01/03/2009")
                        continue
                    break
            except (ValueError, IndexError):
                print("Error: Invalid Date Entered")
                continue
        while True:
            if noneentered is True:
                noneentered = False
                break
            # Get Start time
            try:
                Sinputtime = input("Enter starting time as HH:MM (In 24hr format), if no time is entered, the starting time will default to midnight:")
                if len(Sinputtime) < 1:
                    Sdatetime = Sdate
                    break
                elif len(Sinputtime) > 5:
                    print("Error: Invalid Time Entered")
                    continue
                else:
                    Sinputtime = getnumbers(Sinputtime)
                    Shour = checkfrontzero(Sinputtime[0:2])
                    Sdatetime = datetime(Sdate.year, Sdate.month, Sdate.day, Shour, int(Sinputtime[2:]))
                    if Sdatetime > datetime.now():
                        print("Error: Starting time must be at least 1 minute before current time")
                        continue
                    print("Starting Date and Time: " + str(Sdatetime))
                    break
            except (ValueError, IndexError):
                print("Error: Invalid Time Entered")
                continue

        while True:
            try:
                #Get End Date
                Einputdate = input("Enter End date as MM-DD-YYYY, or press Enter to default to current date and time: ")
                if len(Einputdate) < 1:
                    Edatetime = datetime.now()
                    noneentered = True
                    break
                else:
                    Einputdate = getnumbers(Einputdate)
                    Eyear = int(Einputdate[4:])
                    Emonth = Einputdate[0:2]
                    Eday = Einputdate[2:4]
                    Emonth = checkfrontzero(Emonth)
                    Eday = checkfrontzero(Eday)
                    Edate = datetime(Eyear, Emonth, Eday)
                    if Edate < Sdate:
                        print("Error: End date must be the same or after Start date")
                        continue
                    break
            except (ValueError, IndexError):
                print("Error: Invalid Date Entered")
                continue
        while True:
            if noneentered is True:
                noneentered = False
                break
            try:
                #Get End Time
                Einputtime = input("Enter Ending time as HH:MM (In 24hr format), if no time is entered, the Ending time will default to 11:59:")
                if len(Einputtime) < 1:
                    Edatetime = datetime(Edate.year, Edate.month, Edate.day, 23, 59)
                    break
                elif len(Einputtime) > 5:
                    print("Error: Invalid Time Entered")
                    continue
                else:
                    Einputtime = getnumbers(Einputtime)
                    Ehour = checkfrontzero(Einputtime[0:2])
                    Edatetime = datetime(Edate.year, Edate.month, Edate.day, Ehour, int(Einputtime[2:]))
                    if Sdatetime >= Edatetime > datetime.now():
                        print("Error: Ending time must be after starting time and not after current time: ")
                        continue
                    print("Ending Date and Time: " + str(Edatetime))
                    break
            except (ValueError, IndexError):
                print("Error: Invalid Time Entered")
                continue
        break
    print("Starting Date and Time: " + str(Sdatetime) + " Ending Date and Time: " + str(Edatetime))
    return (int(Sdatetime.timestamp()), int(Edatetime.timestamp()), Sdatetime.replace(tzinfo=pytz.UTC).timestamp(), Edatetime.replace(tzinfo=pytz.UTC).timestamp())'''

### This function gets the start date for the data tables from the user when creating a new crypto in the database
def getStartTime():
    ### Gets unix timestamp of now
    Ctime = int(time.mktime(datetime.now().timetuple()))
    ### 157680000 is 5 years worth of seconds, coinbase has a time limit of somewhere between 5 and 6 years on what data
    ### can be fetched from api
    zerodate = Ctime - 157680000
    start = None
    config = readConfig()
    while True:
        ### Get Start Date
        try:
            Sinput = input("Enter Start date as MM-DD-YYYY, press Enter to default to last date used:")
            if len(Sinput) < 1:
                Sinput = config["lastStartDate"]
                if len(Sinput) < 1:
                    print("Error: No prior start date exists")
                    continue
                Sinputdate = getnumbers(Sinput)
                Syear = int(Sinputdate[4:])
                Smonth = Sinputdate[0:2]
                Sday = Sinputdate[2:4]
                Smonth = checkfrontzero(Smonth)
                Sday = checkfrontzero(Sday)
                Sdate = datetime(Syear, Smonth, Sday)
                if int(time.mktime(Sdate.timetuple())) < zerodate:
                    print("Error: Date Entered must be within 5 years prior")
                    continue
                start = int(Sdate.timestamp())
                config["lastStartDate"] = Sinput
                writeConfig()
                return start, Sinput
            else:
                Sinputdate = getnumbers(Sinput)
                Syear = int(Sinputdate[4:])
                Smonth = Sinputdate[0:2]
                Sday = Sinputdate[2:4]
                Smonth = checkfrontzero(Smonth)
                Sday = checkfrontzero(Sday)
                Sdate = datetime(Syear, Smonth, Sday)
                if int(time.mktime(Sdate.timetuple())) < zerodate:
                    print("Error: Date Entered must be within 6 years prior")
                    continue
                start = int(Sdate.timestamp())
                config["lastStartDate"] = Sinput
                writeConfig()
                return start, Sinput
        except (ValueError, IndexError):
            print("Error: Invalid Date Entered")
            continue

### Fetches 350 candles of data from coinbase api (the max given by Coinbase for individual api calls)
### So this is function is used within loops to make several calls
def getCoinbaseMarketData(RestClient, crypto_market, Start, End, Timeunit, cursor, connection):
    def insertBatch():
        cursor.executemany(f'INSERT OR IGNORE INTO {table} (Unix, Low, High, Open, Close, Volume) VALUES(?, ?, ?, ?, ?, ?)', batch)
        connection.commit()
        batch.clear()
    MarketData = coinbase.rest.RESTClient.get_candles(RestClient, crypto_market, Start, End, Timeunit)
    table = f'{crypto_market.replace('-', '_')}_FIFTEEN_MINUTE_CANDLES'
    i = 0
    batch = []
    ### For some reason data fetched places the oldest candle at the end instead of beginning of dict
    for item in reversed(MarketData['candles']):
        batch.append((item['start'], item['low'], item['high'], item['open'], item['close'], str(int(float(item['volume'])))))
        i += 1
        if i == 50:
            insertBatch()
            i = 0
    insertBatch()
### The 15 min table is the only table that gets data directly from api, and this function handles that
def update15minCandles(acronym, client, cursor, connection):
    end = None
    start = None
    global data, config
    table = from_dict(data[acronym]["tables"]["15min"])
    timeunit = 'FIFTEEN_MINUTE'
    cryptoMarket = acronym + '-USD'
    ### Checks whether this is the first time upating the asset table in question and then prompts the user for start
    ### date to begin fetching data from if it is
    if not data[acronym]['gotData']:
        temp = getStartTime()
        print('Getting data.....this may take a few minutes depending on start date set')
        start = str(temp[0])
        end = str(int(start) + 315000)
        config['lastStartDate'] = temp[1]
        writeConfig()
        print(f"Updating.... {table.name}")
        ### Makes one query again to make sure new inputs work with api before making permanent changes to database.
        try:
            getCoinbaseMarketData(client, cryptoMarket, start, end, timeunit, cursor, connection)
            data[acronym]['gotData'] = True
            data[acronym]['prevStart'] = start
            writeData()
        except Exception as a:
            print(f"An error occurred: {a}")
            connection.rollback()
            quit()

    else:
        ### The function fetches every 15 minute candle, the last candle is rarely a full 15 min
        ### this deletes the last candle of previuous run to fetch the complete candle this run
        cursor.executescript(f'''
                       DELETE FROM {table.name} WHERE Id = (SELECT max(Id) FROM {table.name});
                       UPDATE sqlite_sequence SET seq = (SELECT max(Id) FROM {table.name}) WHERE name = "{table.name}";''')
        print(f"Updating.... {table.name}")

    Ctime = int(time.mktime(datetime.now().timetuple()))
    ### coinbase get_candles requires unix time integers in the form of strings
    while True:
        try:
            cursor.execute(f'SELECT Unix FROM {table.name} WHERE Id = (SELECT max(Id) FROM {table.name})')
            row = cursor.fetchone()[0]
            start = str(int(row) + 1)
            #315000 = the ammount of seconds in 350 15 min candles
            end = str(int(start) + 315000)
            if int(end) > Ctime:
                end = str(Ctime)
                getCoinbaseMarketData(client, cryptoMarket, start, end, timeunit, cursor, connection)
                data[acronym]['prevStart'] = start
                print("Success!")
                break
            getCoinbaseMarketData(client, cryptoMarket, start, end, timeunit, cursor, connection)
            data[acronym]['prevStart'] = start
            continue
        except KeyboardInterrupt:
            print('Program interrupted by user...')
            connection.rollback()
        except Exception as e:
            print(f"An error occurred: {e}")
            connection.rollback()
    writeData()

### Turns MarketDataTable Object into dict in order to store within json file
def to_dict(self):
    return {
        "acronym" : self.acronym,
        "timeunit": self.timeunit,
        "denomination": self.denomination,
        "name": self.name,
     }
### Converts dictionary back to MarketDataTable object
def from_dict(self):
    return MarketDataTable(
        acronym = self["acronym"],
        timeunit = self["timeunit"],
        denomination = self["denomination"],
        name = self["name"]
    )

### Creates default tables that users should want for common trading strategies and analysis
def createDefaultCandleTables(acronym, cursor):
    tables = ["15min", "30min", "1hour", "6hour", "12hour", "1day", "7day", "14day", "30day", "60day", "90day"]
    newTables = dict()
    for table in tables:
        denom = int(re.sub(r'\D+', '', table))
        timeunit = re.sub(r'\d+', '', table)
        newDataTable = MarketDataTable(acronym, timeunit, denom)
        name = newDataTable.name
        newDataTable = to_dict(newDataTable)
        newTables[table] = newDataTable
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
    return newTables




### Updates all other tables with data first obtained in the 15min table without making additional API calls
def updateOtherTable(acronym, sourceTable, table, cursor, connection, iRowLimit=2):
    def maxRow(anyTable):
        cursor.execute(f'SELECT * FROM {anyTable} WHERE Id = (SELECT max(Id) FROM {anyTable})')
        row = cursor.fetchone()
        try:
            maxRow = row[0]
        except TypeError:
            maxRow = 0
        return maxRow
    def getRow(i):
        cursor.execute(f'SELECT * FROM {sourceTable} WHERE Id = ?', (i,))
        row = cursor.fetchone()
        return row
    def insertBatch():
        cursor.executemany(f'INSERT OR IGNORE INTO {table} (Unix, Low, High, Open, Close, Volume) VALUES(?, ?, ?, ?, ?, ?)', batch)
        connection.commit()
        batch.clear()
    print(f"Updating.... {table}")
    ### Delets last row that was likely based on incomplete data of the last row of the 15mintable
    cursor.executescript(f'''
            DELETE FROM {table} WHERE Id = (SELECT max(Id) FROM {table});
            UPDATE sqlite_sequence SET seq = (SELECT max(Id) FROM {table}) WHERE name = "{table}"
        ''')
    ### Ensures program picks up where it left off, even in case of unintended interruption
    startRow = maxRow(table)

    if startRow == 0:
        i = 0
    else:
        i = startRow * iRowLimit
    lastRow = maxRow(sourceTable)
    batch = []
    n = 0
    try:
        ### This loop is for condensing candles into a single candle of longer time period
        while True:
            i += 1
            n += 1
            if i > lastRow:
                break
            ### Unix and Open Values are always taken from 1st row in iteration, the rest will be updated as the current
            ### loop iteration progresses
            row = getRow(i)
            Unix = row[1]
            Low = row[2]
            High = row[3]
            Open = row[4]
            Close = row[5]
            Volume = row[6]
            r = 1
            ### iRowLimit is how many candles from the source table fits into that time period
            ### e.g. 15 min candle source table into 30 min source table, iRowLimit = 2
            while r < iRowLimit:
                if i == lastRow:
                    batch.append((Unix, Low, High, Open, Close, Volume))
                    break
                i += 1
                n += 1
                row = getRow(i)
                Low2 = row[2]
                High2 = row[3]
                if High2 > High:
                    High = High2
                if Low2 < Low:
                    Low = Low2
                Volume = Volume + row[6]
                Close = row[5]
                r += 1
            batch.append((Unix, Low, High, Open, Close, Volume))
            if n >= 50:
                n = 0
                insertBatch()
        insertBatch()
        print("Success!")
    except KeyboardInterrupt:
        print('Program interrupted by user....')
        cursor.execute(f"DELETE FROM TABLE {table} WHERE Id >= {startRow + 1}")
        connection.commit()



