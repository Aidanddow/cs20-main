# Streamline Tables - CS20 Team Project

## Description
Streamline Tables is a web extension for Google Chrome which simplifies the process of downloading tabular data from the web. It can process tables from
- HTML
- PDF's

The project uses Javascript for the frontend, with a Django webapp as the backend.


## Usage
Right click on the desired table, and the data will be downloaded as a .xls file


## Setup

Load Chrome extension in Chrome by going to Settings->Extensions->Load Unpacked, then selecting the project extension folder.


Setup the django models from the backend folder with
```
% rm db.sqlite3
% python manage.py makemigrations streamline
% python manage.py migrate
```
Then run the django webapp with
```
% python manage.py runserver
```

## Run Instructions

Download folder containing extension (Streamline Tables Extension)
Go to chrome://extensions
Enable Developer Mode in top right
Select load unpacked in top left
Navigate to folder and select
Extension should now be installed and can be integrated with

NOTE: this does not need to be done each time you reopen chrome

When updating the code for the extension, the extension automatically updates when you save your changes, no need to redo the steps above

