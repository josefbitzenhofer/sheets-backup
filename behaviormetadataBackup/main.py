import pandas as pd
import sys
from datetime import date
from datetime import datetime
import os
import yaml
from gsheets_importer import *


##################################################################
# JB: Getting the timestamp
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
# JB: Creating a folder for each day
def create_directory(parent_directory: str):
    new_directory = (
        get_timestamp()
    )  # JB: This sets the name of the new folder to the timestamp
    directory_path = os.path.join(parent_directory, new_directory)
    os.makedirs(directory_path)
    print("NOTE: Created new directory @", directory_path)
    return directory_path


#################################################################
# JB: Creating .csv files
def create_csv(spreadsheet_id: str, spreadsheet_title: str, parent_directory: str, header_row: int):
    directory_path = create_directory(parent_directory)
    worksheets = list_worksheets(spreadsheet_id)
    for worksheet in worksheets:
        sheet_name = worksheet
        sheet_df = gsheet2df(spreadsheet_id, sheet_name, header_row)
        file_name = sheet_name + ".csv"
        file_path = os.path.join(directory_path, file_name)
        sheet_df.to_csv(file_path)
    print("NOTE: Backup of", spreadsheet_title, "@", directory_path, "successful.")


##################################################################
# JB: Main code
if __name__ == "__main__":
    with open("config.yaml", "r") as file:
        spreadsheets = yaml.safe_load_all(file)
        for spreadsheet in spreadsheets:
            spreadsheet_title = spreadsheet["spreadsheet_title"]
            spreadsheet_id = spreadsheet["spreadsheet_id"]
            parent_directory = spreadsheet["parent_directory"]
            header_row = spreadsheet["header_row"]
            create_csv(spreadsheet_id, spreadsheet_title, parent_directory, header_row)

    # Exit
    print("NOTE: Graceful exit")
    sys.exit()