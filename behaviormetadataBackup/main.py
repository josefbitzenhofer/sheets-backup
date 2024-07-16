import sys
from datetime import date
from datetime import datetime
import os
import yaml
from gsheets_importer import gsheet2df, list_worksheets


def get_timestamp() -> str:
    """ "Return timestamp"""
    # Get the current date
    today = date.today()
    today = today.strftime("%Y-%m-%d")
    # Get the current time
    time = datetime.now()
    time = time.strftime("%H-%M-%S")

    # Create timestamp
    timestamp = today + "_" + time  # 'YYYY-MM-DD_HH-MM-SS'
    return timestamp


def create_todays_directory(parent_directory: str) -> str:
    """
    Return today's directory
    Args:
        parent_directory (str):         Parent directory path (aka umbrella folder for each day's backup folder)
    Returns:
        str: Today's directory path
    """
    new_directory = get_timestamp()
    # This sets the name of the new folder to the timestamp
    directory_path = os.path.join(parent_directory, new_directory)
    os.makedirs(directory_path)
    print(f"NOTE: Created new directory @ '{directory_path}'.")
    return directory_path


def create_csv(
    spreadsheet_id: str,
    spreadsheet_title: str,
    parent_directory: str,
    header_row: int,
    all_worksheets: bool,
    worksheets_user: list,
) -> None:
    """
    Create folder and CSV files.
    Arg:
        spreadsheet_id (str):           Spreadsheet id
        spreadsheet_title (str):        Spreadsheet title
        parent_directory (str):         Parent directory path (aka umbrella folder for each day's backup folder)
        header_row (int):               Row number of the row with the headers in the worksheets
        all_worksheets (bool):          Either 'True' or 'False' -> if 'True', save all worksheets within a spreadsheet
        worksheets_user (list):         If all_worksheets 'False', take list of worksheets within a spreadsheet to be saved
    Returns:
        None
    Raises:
        AttributeError:                 If gsheet2df returns 'None'
    """
    directory_path = create_todays_directory(parent_directory)
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
        try:
            sheet_df = gsheet2df(spreadsheet_id, sheet_name, header_row)
        except AttributeError as e:
            print(
                f"ERROR: ExceptionError: The worksheet '{sheet_name}' appears to be empty. Exception: '{e}'."
            )
            break
        file_name = sheet_name + ".csv"
        file_path = os.path.join(directory_path, file_name)
        sheet_df.to_csv(file_path)

    print(f"NOTE: Backup of '{spreadsheet_title}' @ '{directory_path}' successful.")


def main():
    """
    Get config from 'config.yaml' file.
    Iterate over each worksheet to be saved, turn it into .csv file.
    Returns:
        None
    Raises:
        FileNotFoundError:              If the parent directory does not exists
        ValueError:                     If a value within the 'config.yaml' file has not properly been set up
    """
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
                    if not os.path.isdir(parent_directory):
                        raise FileNotFoundError(
                            f"ERROR: The directory '{parent_directory}' does not exist."
                        )
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
            except Exception as e:
                raise ValueError(
                    f"ERROR: ExceptionError: You did not correctly set up your 'config.yaml' file for '{spreadsheet_title}.'"
                ) from e


if __name__ == "__main__":
    main()
    print("NOTE: Graceful exit.")
    sys.exit()
