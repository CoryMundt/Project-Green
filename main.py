### Purpose of this application is to fetch data from coinbase in order to build and edit a database of crypto prices
import subprocess
import sys
from pathlib import Path
from PGfunctions import readConfig, writeConfig
venv_python = Path(sys.executable)
config = readConfig()
try:
    ### config[runs] is the amount the of times the program has been run, its initialized to -1 to show the program
    ### has never run before. This is because BackupDataTables.py needs to ask the user how often they want to backup
    ### based on config['runs'] but config[runs]is reset to 0 every time a backup is created and we only want to ask
    ### the user once when they first use the program
    if config['runs'] == -1:
        config['runs'] = 0
        writeConfig()
        ### Asks user for a crypto(s) they want price data for added to the database
        subprocess.run([venv_python, "CreateNewCrypto.py"])
        ### Asks user how often they want to back up which is determined by config[runs] aka how many times the program
        ### has run and therefore how many times the database has been updated
        subprocess.run([venv_python, "BackupDatabase.py"])
        ### Allows user to create custom time period price tables not included by default
        subprocess.run([venv_python, "BuildDataTables.py"])
        ### Allows user to delete tables they do not need without delteting a whole asset, this python file is included
        ### on the first loop because there are tables created by default the user may not want
        subprocess.run([venv_python, "DeleteTables.py"])
    else:
        ### Fetches data from coinbase and updates the database, it is called first because in case the program
        ### is interrupted it must finish updating before the user makes any changes to the table this file is also
        ### called to run within other files
        subprocess.run([venv_python, "UpdateTables.py"])
        subprocess.run([venv_python, "CreateNewCrypto.py"])
        subprocess.run([venv_python, "BuildDataTables.py"])
        subprocess.run([venv_python, "DeleteTables.py"])
        ### Asks user if they want to remove a crypto, and all tables associated with that crypto, from the database
        subprocess.run([venv_python, "DeleteCrypto.py"])
        ### Same file as above, but in additon asking the user how often they want to create a backup, on the first run
        ### it also executes the creation of the backup itself
        subprocess.run([venv_python, "BackupDatabase.py"])
except Exception as e:
    print(f"Something went wrong: {e} ...")
    subprocess.run([venv_python, "RestoreFromBackup.py"])