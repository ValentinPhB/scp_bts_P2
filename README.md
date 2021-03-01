# scraping_bts BETA VERSION
## Table of contents

1. [Technologies](#1-technologies)
2. [General information](#2-general-information)
3. [Installation Python](#3-installation-python)
4. [Setup](#4-setup)
	- [Setup for Unix](#a-setup-for-unix)
 	- [Setup for Windows](#b-setup-for-windows)
5. [Open data](#5-open-data)
6. [Author](#6-author)

## 1. Technologies

Project is created with Python 3.8.6.

- beautifulsoup4==4.9.3
- bs4==0.0.1
- certifi==2020.12.5
- chardet==4.0.0
- idna==2.10
- lxml==4.6.2
- numpy==1.20.1
- pandas==1.2.2
- progress==1.5
- python-dateutil==2.8.1
- pytz==2021.1
- requests==2.25.1
- six==1.15.0
- soupsieve==2.2
- urllib3==1.26.3

## 2. General information

scraping_bts contain 'main.py', a Python script to collect information from the web site "Books to scrape" (bts).

This scipt, main.py, will create two directories named "bts_csv" and "images_bts" respectively.
If those directories already exist, main.py will remove them before recreate new ones.

From "Books to scrape" website url, main.py will extract all URLs books for a category, transform all information needed and load it in csv files.
This actions will be executed for all categories of books in "books to scrape". Csv files will be named '"category".csv.' and redirected to "bts_csv".
It will also download all images and redirect it to "images_bts".

The informations collected are :

* product_page_url
* universal_ product_code (upc)
* title
* price_including_tax
* price_excluding_tax
* number_available
* product_description
* category
* review_rating
* image_url
* image_localisation


## 3. Installation Python

Project is created with Python 3.8.6.

First download Python.exe from https://www.python.org/downloads/ for the 3.8.6 Python version __or above__ and execute it. 
After installing Python.exe please see the appropriate guide for your operating System.

## 4. Setup
### A) *Setup for Unix*

After downloading scp_bts_P2-main.zip from Github, extract it to a location of your choice (exemple : "PATH").
Or if you use git, clone it from https://github.com/ValentinPhB/scp_bts_P2.git

Create a virtual environment in "PATH" and install packages from requirements.txt.
```
$ cd ../path/to/scp_bts_P2
$ python3 -m venv env
$ source env/bin/activate
$ python3 -m pip install -U pip
$ pip install -r requirements.txt
```

#### *Execute main.py for Unix* 
```
$ python3 main.py
```

### B) *Setup for Windows* 

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

#### *Execute main.py for Windows*
```
$ ENV\Scripts\python.exe main.py
```

## 5. Open Data
### *With Microsoft Excel*

- Open Microsoft Excel
- Go to NEW >> DATA >> Get External Data >> From Text
- Go to the location of the CSV file, that you want to import.
- Choose Delimited.
- Set the character encoding to 65001: Unicode (UTF-8) from the dropdown list.
- Check My data has headers.
- Click next to display the second step of Text Import Wizard.

- Set the delimiter to a comma only.
- Click next to move to the third step.

- Click OK and then Finish.

- Keep the default values inside the Import Data window and click OK.

### *With Google Sheets*

- Open Google Sheets
- Choose “File” → “Import” → “Upload” → “Select a file from your computer.”
- Choose your CSV file from your Documents or Desktop folder.
- in the following window, Choose “Import data.”

## 6. Author

Valentin Pheulpin


