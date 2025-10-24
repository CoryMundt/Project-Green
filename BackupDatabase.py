import shutil
from PGfunctions import readConfig, writeConfig
### Counts how many times the program has run and on  first run asks how many runs user wants before updating backup
### database. When creating a backup it copies the file MarketData.sqlite to MarketDataBackup.sqlite
config = readConfig()
while True:
    if config['runs'] == -1:
        backupRun = input("How many times after updating should we create a back up for the database? Press Enter to default to 50: ")
        try:
            ### If user doesn't enter a number, e.g. pressing enter, the backupRun defaults to 50 and intial backup files
            ### are created by copying the main files
            if len(backupRun) < 1:
                backupRun = 50
                shutil.copy('MarketData.sqlite', 'MarketDataBackup.sqlite')
                shutil.copy('Sdata.json', 'SdataBackup.json')
                shutil.copy('config.json', 'configBackup.json')
            backupRun = int(backupRun)
            config['backupRun'] = backupRun
            # In case a user enters 0
            if backupRun < 1:
                print("You must create a backup database in case something unexpected happens")
                continue
            config['runs'] = 0
        except TypeError:
            print("Error: Numbers are accepted only")
            continue
    break

if config['runs'] >= config["backupRun"]:
    shutil.copy('MarketData.sqlite', 'MarketDataBackup.sqlite')
    shutil.copy('Sdata.json', 'SdataBackup.json')
    shutil.copy('config.json', 'configBackup.json')
    config['runs'] = 0
    writeConfig()
