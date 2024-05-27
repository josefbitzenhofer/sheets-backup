import gspread
import pandas as pd
import sys
from datetime import date
from datetime import datetime
import os

##################################################################
# Opening the Google Spreadsheet
gc = gspread.oauth()                                                                    # Authenticating with the created credentials
sh = gc.open("Behaviour metadata")                                                      # Opening the Google Sheet

##################################################################
# Getting the timestamp
def get_timestamp():
    # JB: get the current date
    today = date.today()
    today = today.strftime("%Y-%m-%d")
    # JB: get the current time
    time = datetime.now()
    time = time.strftime("%H-%M-%S")

    # JB: Create timestamp
    timestamp = today + "_" + time  # JB: 'YYYY-MM-DD_HH-MM-SS'
    return timestamp

##################################################################
# Creating a folder for each day
def get_parent_directory():
    config_file = open("config.txt", "r")                                       # JB: opens the config.txt file
    parent_directory = config_file.read()                                       # JB: sets the parent directory to the path in the config.txt
    return parent_directory

def create_directory():
    parent_directory = get_parent_directory()                                   # JB: This is the parent directory of the backup
    new_directory = get_timestamp()                                             # JB: This sets the name of the new folder to the timestamp                                                       # JB: Globalling the directory path
    directory_path = os.path.join(parent_directory, new_directory)
    os.makedirs(directory_path)
    print("NOTE: Created new directory @", directory_path)
    return directory_path


##################################################################
# Creating the directory
get_timestamp()
directory_path = create_directory()

##################################################################
# Setting our worksheets
worksheet_list = sh.worksheets()                                                        # Getting a list of worksheets we can iterate over

for worksheet in worksheet_list:
    worksheet_df = pd.DataFrame(worksheet.get_all_records())                            # Getting all data of the worksheet into a Pandas dataframe
    # Setting the filename
    file_name = worksheet.title + ".csv"
    file_path = os.path.join(directory_path, file_name)
    # Dumping the Pandas dataframe into a .csv file
    worksheet_df.to_csv(file_path)

# Exit
print("NOTE: Graceful exit")
sys.exit()