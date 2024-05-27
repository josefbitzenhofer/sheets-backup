# Viral: metadata Backup

## Pre-requisites
You need to set up a few things:
- **Python**
- **Server connection**
- **config.txt**
- **Google API connection**

### Python
- gspread
- pandas 

See 'requirements.txt'.

You can either:  
1) Use the `bmB_venv` venv provided.  
2) Create a venv, activate it and install the modules into it.

### Server connection
Make sure that you are **connected** to the **"MarcBusche"-server**!
(When you are running your machine from outside the UCL network, make sure you are connected via the UCL VPN!)

### config.txt
Set up the `config.txt` file:  
Open the `config.txt` file within the umbrella folder the in your text editor.  
> The file's content looks like this:
```
    [Configuration]
    sh_title: Behaviour metadata
    parent_directory: /Volumes/MarcBusche/Josef/behaviormetadataBackup/data
```
   
> If need be, change the settings:  
> `'sh_title` refers to the exact title of the spreadsheet. The title has to match exactly and you have to have access to said spreadsheet (either shared or owned).
> `'parent_directory'` refers to the directory path of the server folder where you want to save the backups.  

> Note: Make sure each entry consists of **only one line**! Otherwise Python will prompt an error.  
> Also, do not use quotes (" ") or single quotes (' ') here.

#### MacOS  
The directory path should look something like this:  
`/Volumes/MarcBusche/Josef/behaviormetadataBackup/data`  

#### Linux
The directory path should look something like this:  
`/mnt/MarcBusche/Josef/behaviormetadataBackup/data`  
Or this:  
`/media/MarcBusche/Josef/behaviormetadataBackup/data`

### Google API connection
See the 'Client credentials' section of this [tutorial](https://gspread-pandas.readthedocs.io/en/latest/getting_started.html#installation-usage) for how to establish the connection.  
> Note: Use the **same** Google account which has access to the spreasheet!

## Setting up the Cron job
### Step 1:
For setting up the Cron job, open your **Terminal**.  
Enter `crontab -e`.  
Press `I` on your keyboard to enter the insert mode.

### Step 2:
> Note: Replace `'PATHNAME'` with the path where you saved the umbrella folder.  
> Note: Replace `'PATHtoPYTHON'` with the path to the **venv** `python3`! This can be the `python3` in the`bmB_venv` venv, if you decided to use this one.
#### MacOS
Might look something like `/Users/username/Documents/venv/bin/python3`.  
#### Linux
Might look something like `/home/username/Documents/venv/bin/python3`.  

  
Please enter:  
`00 11 * * * PATHtoPYTHON PATHNAME/behaviormetadataBackup/behaviormetadataBackup/main.py`

### Step 3:
Then press `esc` on your keyboard.  
Enter `:wq` and press `enter` to leave the editor.  
> Note: Sometimes, you will be prompted to allow the edits. (MacOS)  
> Note: The first time you have to give Python access to your files and your network. (MacOS)  

In summary, `main.py` will be running **every day** at **11 am**.

### Pro tips:
> You can check if you set up the cronjob correctly by entering `crontab -l` into your terminal.  
It should show the cronjob for the backup which you hopefully just set up.  

> You can **delete** the cronjob by repating steps 1 and 2. Just erase the cron job command.  

> If you want to change the time and date of the cronjob, see this [tutorial](https://medium.com/@justin_ng/how-to-run-your-script-on-a-schedule-using-crontab-on-macos-a-step-by-step-guide-a7ba539acf76) for guidance.