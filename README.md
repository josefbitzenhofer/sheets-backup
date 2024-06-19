# Viral: metadata Backup

## Pre-requisites
You need to set up a few things:
- **Python**
- **Server connection**
- **config.yaml**
- **Google API connection**

### Python
- Google API
- pandas
- pathlib
- pickle
- pyyaml 

See 'requirements.txt'.

You can either:  
1) Use the `bmB_venv` venv provided.  
2) Create a venv, activate it and install the modules into it.

### Server connection
Make sure that you are **connected** to the **"MarcBusche"-server**!
(When you are running your machine from outside the UCL network, make sure you are connected via the UCL VPN!)

### config.yaml
Set up the `config.yaml` file:  
Open the `config.yaml` file within the umbrella folder in your text editor.  
> The file's content looks like this:
```
    ---
    spreadsheet_title: Behaviour metadata
    spreadsheet_id: 1fMnVXrDeaWTkX-TT21F4mFuAlaXIe6uVteEjv8mH0Q4
    parent_directory: /Volumes/MarcBusche/Josef/backup/data/behaviormetadataBackup
    header_row: 1
    ---
    spreadsheet_title: mouse metadata
    spreadsheet_id: 1QVkoP9g2XUB8OBu4Hs4d2h3ebUQx2sAeQ4wMnlLhbv8
    parent_directory: /Volumes/MarcBusche/Josef/backup/data/mousemetadataBackup
    header_row: 1
```
   
> If need be, change the settings.
> You can easily **add new spreadsheets** to the `config.yaml` file!  
> The spreadsheet data has to be formatted as follows:  
```
    ---
    spreadsheet_title: YOUR-spreadsheet_title
    spreadsheet_id: YOUR-spreadsheet_id
    parent_directory: YOUR-parent_directory
    header_row: YOUR-header_row
```  
> **Important note**: You need the dashes (`---`) to start a new section for another spreadsheet!  

> `'spreadsheet_title` refers to the title of the spreadsheet.  
> This key: value pair is not needed by the code. It is merely to help you keep track of your spreadsheets.  
   
>`'spreadsheet_id` refers to the ID of the spreadsheet. This has to be **accurate**!  
> You will find your spreadsheet's ID here: `https://docs.google.com/spreadsheets/d/SPREADSHEET_ID`  
> Additionally, you have to have access to said Google spreadsheet (either shared or owned).   
   
> `'parent_directory'` refers to the directory path of the server folder where you want to save the backups.  
> See the section below on how to adjust the directory path depending on the machine you are using. 
    
> `'header_row'` is the number of the row which contains the headers of the columns.   
> This must be an **integer**, e.g. `1`. This information tells our code to look for the headers in the said row of the sheet.

> Note: Make sure each entry consists of **only one line**! Otherwise Python will prompt an error.  
> Also, do not use quotes (" ") or single quotes (' ') here.

#### MacOS  
The directory path should look something like this:  
`/Volumes/MarcBusche/Josef/backup/data/behaviormetadataBackup`  

#### Linux
The directory path should look something like this:  
`/mnt/MarcBusche/Josef/backup/data/behaviormetadataBackup`  
Or this:  
`/media/MarcBusche/Josef/backup/data/behaviormetadataBackup`   
   
   
> This can obviously differ, if you decide to store your data elsewhere.

### Google API connection
See this [tutorial](https://developers.google.com/sheets/api/quickstart/python) for how to establish the connection.  
> Note: Use the **same** Google account which has access to the spreadsheet!  

Important points about this one (sorry - here it gets ugly):  
- Follow the instructions in the tutorial linked above.
- It is **crucial** that you move the `credential.json` file to your working directory.
(I.e., into the umbrella folder: `PATHNAME/behaviormetadataBackup/credentials.json`)  
- Note that, when you run the script for the first time, you will be asked to sign in to your Google account.
Afterwards, your token will be saved and you will only be asked to repeat the sign in process if your token expires.

## Setting up the Cron job
### Step 1:
For setting up the Cron job, open your **Terminal**.  
Enter `crontab -e`.  Press `enter` on your keyboard.
Press `I` on your keyboard to enter the insert mode.

### Step 2:
> Note: Replace `'PATHNAME'` with the path where you saved the umbrella folder.  
> Note: Replace `'PATHtoPYTHON'` with the path to the **venv** `python3`! This can be the `python3` in the`bmB_venv` venv, if you decided to use this one.
#### MacOS
Might look something like `/Users/username/Documents/bmB_venv/bin/python3`.  
#### Linux
Might look something like `/home/username/Documents/bmB_venv/bin/python3`.  

  
Please enter or copy and paste:  
`00 11 * * * PATHtoPYTHON PATHNAME/behaviormetadataBackup/behaviormetadataBackup/main.py`

### Step 3:
Then press `esc` on your keyboard.  
Enter `:wq` and press `enter` on your keyboard to leave the editor.  
> Note: Sometimes, you will be prompted to allow the edits. (MacOS)  
> Note: The first time, you have to give Python access to your files and your network. (MacOS)  

In summary, `main.py` will be running **every day** at **11 am**.

### Pro tips:
> You can check if you set up the cronjob correctly by entering `crontab -l` into your terminal and pressing `enter` on your keyboard.  
It should show the cronjob for the backup which you just set up.  

> You can **delete** the cronjob by repeating steps 1 and 2. Just erase the cron job command.  

> If you want to change the time and date of the cronjob, see this [tutorial](https://medium.com/@justin_ng/how-to-run-your-script-on-a-schedule-using-crontab-on-macos-a-step-by-step-guide-a7ba539acf76) for guidance.

## Most important note at the end
If I were you, I would firmly recommend that you **run the script the first time from a text editor** (e.g. VS Code, Atom, ...), IDE or simply via your terminal.  
Just think of all the 'firsts' described above.  
You do not want your machine to prompt all of the requests to set up the task which will secure your presumably most vital data while you are wandering around, clueless... ;)