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
    print(f"NOTE: Created new directory @ '{directory_path}'.")
    return directory_path


#################################################################
# JB: Creating .csv files
def create_csv(
    spreadsheet_id: str,
    spreadsheet_title: str,
    parent_directory: str,
    header_row: int,
    all_worksheets: bool,
    worksheets_user: list,
):
    directory_path = create_directory(parent_directory)
    # This checks if the user wants all worksheets within the spreadsheet to be saved. Else, it takes the worksheets the user specified.
    worksheets = []
    if all_worksheets:
        worksheets = list_worksheets(spreadsheet_id)
    else:
        worksheet_names = worksheets_user
        for worksheet_name in worksheet_names:
            # If the sheet name contains numbers, it must be enclosed in single quotes # JB: We have to deal with blank spaces as well.
            if any(char.isdigit() for char in worksheet_name) or any(
                char.isspace() for char in worksheet_name
            ):
                worksheet_name = f"'{worksheet_name}'"
                worksheets.append(worksheet_name)
    for worksheet in worksheets:
        sheet_name = worksheet
        sheet_df = gsheet2df(spreadsheet_id, sheet_name, header_row)
        file_name = sheet_name + ".csv"
        file_path = os.path.join(directory_path, file_name)
        try:
            sheet_df.to_csv(file_path)
        except:
            print(
                f"ERROR: ExceptionError - Worksheet '{sheet_name}' could not be saved."
            )
    print(f"NOTE: Backup of '{spreadsheet_title}' @ '{directory_path}' successful.")


##################################################################
# JB: Main code
if __name__ == "__main__":
    with open("config.yaml", "r") as file:
        spreadsheets = yaml.safe_load_all(file)
        for spreadsheet in spreadsheets:
            try:
                spreadsheet_title = spreadsheet["spreadsheet_title"]
                active = spreadsheet["active"]
                if active:
                    print(f"NOTE: Starting backup for '{spreadsheet_title}'.")
                    spreadsheet_id = spreadsheet["spreadsheet_id"]
                    parent_directory = spreadsheet["parent_directory"]
                    header_row = spreadsheet["header_row"]
                    all_worksheets = spreadsheet["all_worksheets"]
                    if not all_worksheets:
                        worksheets_user = spreadsheet["worksheets"]
                        create_csv(
                            spreadsheet_id,
                            spreadsheet_title,
                            parent_directory,
                            header_row,
                            all_worksheets,
                            worksheets_user,
                        )
                    else:
                        worksheets_user = []
                        create_csv(
                            spreadsheet_id,
                            spreadsheet_title,
                            parent_directory,
                            header_row,
                            all_worksheets,
                            worksheets_user,
                        )
                else:
                    print(
                        f"NOTE: No backup for '{spreadsheet_title}'. `active` is set to `{active}`."
                    )
            except:
                print(
                    f"ERROR: ExceptionError - you did not correctly set up your 'config.yaml' file for '{spreadsheet_title}'."
                )
    # Exit
    print("NOTE: Graceful exit.")
    sys.exit()
