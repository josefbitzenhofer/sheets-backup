# Viral: metadata Backup

## Pre-requisites
You need to set up a few things:
- **Python**
- **Server connection**
- **Google API connection**

### Python
- gspread
- pandas 

See 'requirements.txt'.

Install them into a venv and activate it.

### Server connection
Make sure that you are **connected** to the **"MarcBusche"-server**!
(When you are running your machine from outside the UCL network, make sure you are connected via the UCL VPN!)

### Google API connection
See the 'Client credentials' section of this [tutorial](https://gspread-pandas.readthedocs.io/en/latest/getting_started.html#installation-usage) for how to establish the connection.

## Setting up the Cron job
### Step 1:
For setting up the Cron job, open your **Terminal**.
Enter `crontab -e`.
Press `I` on your keyboard to enter the insert mode.

### Step 2:
Note: Replace 'PATHNAME' with the path where you saved the umbrella folder.
Note: Replace 'PATHtoPYTHON' with the path to the **venv** Python! (Might look something like `/Users/username/Documents/behaviormetadataBackup/.venv/bin/python3`)  
Please enter:  
`00 11 * * * PATHtoPYTHON PATHNAME/behaviormetadataBackup/behaviormetadataBackup/main.py`

### Step 3:
Then press `esc` on your keyboard.
Enter `:wq` and press `enter` to leave the editor.
Note: Sometimes, you will be prompted to allow the edits.
Note: The first time you have to give Python access to your files and your network.

This means, that `main.py` will be running **every day** at **11 am**.

### Pro tips:
> You can check if you set up the cronjob correctly by entering `crontab -l` into your terminal.
It should show the cronjob for the backup which you hopefully just set up.

> You can **delete** the cronjob by repating steps 1 and 2. Just erase the cron job command.

> If you want to change the time and date of the cronjob, see this [tutorial](https://medium.com/@justin_ng/how-to-run-your-script-on-a-schedule-using-crontab-on-macos-a-step-by-step-guide-a7ba539acf76) for guidance.