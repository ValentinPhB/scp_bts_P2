# scraping_bts
## Table of contents
* [General info]
* [Technologies]
* [Setup for Unix]
* [Setup for Windows]
* [Load data]

## Technologies
Project is created with:

* beautifulsoup4==4.9.3
* bs4==0.0.1
* certifi==2020.12.5
* chardet==4.0.0
* idna==2.10
* lxml==4.6.2
* pkg-resources==0.0.0
* requests==2.25.1
* soupsieve==2.2
* urllib3==1.26.3
* wget==3.2


## General info 
scraping_bts contain 'main.py', a Python script to collect information from the web site "Books to scrape" (bts).

This scipt, main.py, will create two directories named "bts_csv" and "images_bts" respectively.
If those directories already exist, main.py will remove them before recreate new ones.

From "Books to scrape" website url, main.py will create differents csv files for all categories of books and redirect them to "bts_csv".
It will also download all images and redirect it to "images_bts".

The informations collected are :

product_page_url
universal_ product_code (upc)
title
price_including_tax
price_excluding_tax
number_available
product_description
category
review_rating
image_url
image_localisation


Please see the appropriate guide for your operating System.


## a. Setup for Unix 
After downloading scp_bts_P2-main.zip from Github, extract it to a location of your choice (exemple : "PATH").
Or if you use git, clone it from https://github.com/ValentinPhB/scp_bts_P2.git

If pip isn't installed :
```
$ sudo apt update
$ sudo apt install python3-pip
```

If pip is already installed, create a virtual environment in "PATH" and install packages from requirements.txt.
```
$ cd ../path/to/scp_bts_P2
$ python3 -m venv env
$ source env/bin/activate
$ python3 -m pip install -U pip
$ pip install -r requirements.txt
```

### b. Execute main.py for Unix 
```
$ python3 main.py
```

## a. Setup for Windows 
After downloading scp_bts_P2-main.zip from Github, extract it to a location of your choice (exemple : "PATH").
Or if you use git, clone it from https://github.com/ValentinPhB/scp_bts_P2.git

Then, using cmd, go to "PATH", create a virtual environment and install packages from requirements.txt.
```
$ CD ../path/to/scp_bts_P2
$ python3 -m venv env
$ env\Scripts\activate.bat
$ py -m pip install -U pip
$ pip install -r requirements.txt
```

### b. Execute main.py for Windows
```
$ ENV\Scripts\python.exe main.py
```

## Load Data
### With Microsoft Excel
* Open Microsoft Excel
* Go to DATA >> Get External Data >> From Text
* Go to the location of the CSV file, that you want to import.
* Choose Delimited.
* Set the character encoding to 65001: Unicode (UTF-8) from the dropdown list.
* Check My data has headers.
* Click next to display the second step of Text Import Wizard.
* Set the delimiter to a comma.
* Click next to move to the third step.
* Click OK and then Finish.
* Keep the default values inside the Import Data window and click OK.

### With Google Sheets
* Open Google Sheets
* Choose “File” → “Import” → “Upload” → “Select a file from your computer.”
* Choose your CSV file from your Documents or Desktop folder.
* in the following window, Choose “Import data.”




