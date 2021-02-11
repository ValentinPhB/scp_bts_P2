# scrap_books_to_scrape
scrap_books_to_scrape contain main.py, a Python script to collect information from the web site "Books to scrape".

This scipt, main.py, will create two directories named "books_to_scrape" and "images_books_to_scrape" respectively.
If those directories already exist, main.py will remove them before recreate new ones.

From "Books to scrape" website url, main.py will create differents csv files for all categories of books and redirect them to "books_to_scrap".
It will also download all images and redirect it to "images_books_to_scrape".

The informations collect are :

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

## Installation virtual environment Python3

After downloading scp_bts_P2-main.zip from Github, extract it to a location of your choice (exemple : "PATH").
Or if you use git, clone it from https://github.com/ValentinPhB/scp_bts_P2.git

Then, using terminal and go to "PATH", create a virtual environment and install packages from requirements.txt
```
$ cd ../path/to/scp_bts_P2
$ python3 -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt
```

## Execute main.py

```
$ python3 main.py
```

