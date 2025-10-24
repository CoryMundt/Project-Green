### In the event something unexpected goes wrong, this file allows the user to restore from the backup
### by copying MarketDataBackup.sqlite file to MarketData.sqlite
import shutil
while True:
    answer = input("Would you like to restore from Backup? Y/N: ")
    if answer.upper() == "Y":
        answer = input("Are you sure you would like to restore from Backup? Y/N: ")
        if answer.upper() == "Y":
            shutil.copy('MarketDataBackup.sqlite', 'MarketData.sqlite')
            shutil.copy('SdataBackup.json', 'Sdata.json')
            shutil.copy('configBackup.json', 'config.json')
            print("Restored from backup")
            break
        elif answer.upper() == "N":
            break
        else:
            print("Enter Y or N")
            continue
    elif answer.upper() == "N":
        break
    else:
        print("Enter Y or N")
        continue
