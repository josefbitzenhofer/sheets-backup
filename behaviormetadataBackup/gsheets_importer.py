import pickle
import os.path


from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pandas as pd

from pathlib import Path

# JB: Sets "HERE" to the parent of this file's path
HERE = Path(__file__).parent

# JB: Smart. Sets the path to the parent of the parent of the file.
CRED_PATH = HERE.parent / "credentials.json"
TOKEN_PATH = HERE.parent / "token.pickle"


def credentials(spreadsheet_id: str):
    # JB:
    # It takes the spreadsheet_id, uses the credentials or prompts the credeting process, then returns the 'service'.

    creds = None
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, "rb") as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CRED_PATH, SCOPES)
            # JR - this is needed to authenticate through ssh
            # flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(TOKEN_PATH, "wb") as token:
            pickle.dump(creds, token)

    service = build("sheets", "v4", credentials=creds, cache_discovery=False)

    return service


def list_worksheets(spreadsheet_id: str):
    # JB: It takes a spreadsheet_id and returns a list of worksheets we can iterate over to create .csv files.
    service = credentials(spreadsheet_id)
    spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
    sheets = spreadsheet.get("sheets", [])
    worksheets = []

    for sheet in sheets:
        sheet_name = sheet["properties"]["title"]
        # If the sheet name contains numbers, it must be enclosed in single quotes # JB: We have to deal with blank spaces as well.
        if any(char.isdigit() for char in sheet_name) or any(
            char.isspace() for char in sheet_name
        ):
            sheet_name = f"'{sheet_name}'"
        worksheets.append(sheet_name)

    return worksheets


def build_gsheet(spreadsheet_id: str, sheet_name: str):
    # JB: It takes the sheet_name and returns the gsheet object.
    service = credentials(spreadsheet_id)
    sheet = service.spreadsheets()

    return sheet.values().get(spreadsheetId=spreadsheet_id, range=sheet_name).execute()


def gsheet2df(spreadsheet_id: str, sheet_name: str, header_row: int):
    # JB: It takes the gsheet from the build_gsheet subroutine and returns a pandas dataframe.
    gsheet = build_gsheet(spreadsheet_id, sheet_name)
    values = gsheet.get("values", [])

    try:
        num_columns = max(len(row) for row in values)

        header_data = values[
            header_row - 1
        ]  # JB: Accounting for the fact, that python starts counting at 0.
        # JB: Trying to prevent errors with empty header data.
        for i in range(len(header_data)):
            if not header_data[i]:
                header_data[i] = ""
        # Also ensuring the header row is as long as the longest row in the entire sheet
        column_names = header_data
        if len(column_names) < num_columns:
            column_names.extend([""] * (num_columns - len(column_names)))

        # JB: Setting up the actual cell data, assuming, it starts one row beneath the header row
        cell_data = values[header_row:]
        # JB: Copied from API code?
        # corrects for rows which end with blank cells
        for i, row in enumerate(cell_data):
            if len(row) < num_columns:
                row.extend([""] * (num_columns - len(row)))

        # JB: Now creating our Pandas dataframe
        gsheetdf = pd.DataFrame(cell_data, columns=column_names)

        return gsheetdf

    except:
        print(f"ERROR: ExceptionError - No data found for worksheet '{sheet_name}'.")
