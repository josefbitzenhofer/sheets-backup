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

Create a venv, activate it and install the modules into it.

### Server connection
Make sure that you are **connected** to the **"MarcBusche"-server**!
(When you are running your machine from outside the UCL network, make sure you are connected via the UCL VPN!)

### config.txt
Set up the `config.txt`file:  
Open the `config.txt` file within the umbrella folder the in your text editor.
Copy the path of the backup directory into the `config.txt` file and save the change.  

#### MacOS  
It should look something like this:  
`/Volumes/MarcBusche/Josef/behaviormetadataBackup/data`  

#### Linux
It should look something like this:  
`/mnt/MarcBusche/Josef/behaviormetadataBackup/data`  
Or this:  
`/media/MarcBusche/Josef/behaviormetadataBackup/data`
  

> Note: Make sure the file consists of **only one line**! Otherwise Python will prompt an error.

### Google API connection
See the 'Client credentials' section of this [tutorial](https://gspread-pandas.readthedocs.io/en/latest/getting_started.html#installation-usage) for how to establish the connection.

## Setting up the Cron job
### Step 1:
For setting up the Cron job, open your **Terminal**.
Enter `crontab -e`.
Press `I` on your keyboard to enter the insert mode.

### Step 2:
Note: Replace 'PATHNAME' with the path where you saved the umbrella folder.
Note: Replace 'PATHtoPYTHON' with the path to the **venv** Python!
#### MacOS
Might look something like `/Users/username/Documents/venv/bin/python3`.  
#### Linux
Might look something like `/home/username/Documents/venv/bin/python3`.  

  
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