import gspread
import pandas as pd
import sys
from datetime import date
from datetime import datetime
import os
import yaml

##################################################################
# Opening the Google Spreadsheet
def open_spreadsheet(sh_title):            
    gc = gspread.oauth()  # Authenticating with the created credentials
    sh = gc.open(sh_title)  # Opening the Google spreadsheet
    return sh

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
def create_directory(parent_directory):
    new_directory = (
        get_timestamp()
    )  # JB: This sets the name of the new folder to the timestamp
    directory_path = os.path.join(parent_directory, new_directory)
    os.makedirs(directory_path)
    print("NOTE: Created new directory @", directory_path)
    return directory_path

##################################################################
# Creating .csv files
def create_csv(sh, parent_directory):
    worksheet_list = sh.worksheets()                        # Getting a list of worksheets we can iterate over
    directory_path = create_directory(parent_directory)
    for worksheet in worksheet_list:
        worksheet_df = pd.DataFrame(
            worksheet.get_all_values()
        )  # Getting all data of the worksheet into a Pandas dataframe
        # Setting the filename
        file_name = worksheet.title + ".csv"
        file_path = os.path.join(directory_path, file_name)
        # Dumping the Pandas dataframe into a .csv file
        worksheet_df.to_csv(file_path)
    print("NOTE: Backup of", sh_title, "@", directory_path, "successful.")

##################################################################
# Main code
with open("config.yaml", "r") as file:
        # Getting the variables from the config.yaml file
        spreadsheets = yaml.safe_load_all(file)

        for spreadsheet in spreadsheets:
            # Get the variables for every spreasheet
            sh_title = spreadsheet["sh_title"]
            parent_directory = spreadsheet["parent_directory"]
            # Then open spreadsheet and create the backup
            sh = open_spreadsheet(sh_title)
            create_csv(sh, parent_directory)

# Exit
print("NOTE: Graceful exit")
sys.exit()