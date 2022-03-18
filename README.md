# Streamline Tables - CS20 Team Project

## Description
Streamline Tables is a web extension for Google Chrome which simplifies the process of downloading tabular data from the web. It can process tables from
- HTML
- PDF's

The project uses Javascript for the frontend, with a Django webapp as the backend.


## Usage
Right click on the desired table, and the data will be downloaded as a .xls file


## Setup

Load Chrome extension in Chrome by going to Settings->Extensions->Load Unpacked, then selecting the project extension folder.\
Running the Django app backend requires python version 3.8 or later, this can be found here - https://www.python.org/downloads/


### Automatically - Windows 

The First time you download the file run the Install.bat file - this will install all the python packages for the backend.\
Then when you want to run the Streamline Table run the Start.bat file - While the terminal is running you will be able to use the extension freely. 

### Automatically - Mac 



### Manually 
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

Download the folder extension,
Go to chrome://extensions
Enable Developer Mode in top right
Select load unpacked in top left
Navigate to folder and select
Extension should now be installed

NOTE: this does not need to be done each time you reopen chrome\
NOTE: Does not work unless server is running 

When updating the code for the extension, the extension automatically updates when you save your changes, no need to redo the steps above

## Information on the Django backend - run with Start.bat files

This only needs to be running on one machine on a wifi network and the extension will work on all other machines on the same wifi network.\
It could also be setup to be hosted by one machine and be made public so that any machine on any network can access it with having to run the Start file. More information here - https://docs.djangoproject.com/en/3.2/howto/deployment/

