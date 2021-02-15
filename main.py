#!/usr/bin/env python

from bs4 import BeautifulSoup
import csv
import os
import requests
import shutil
import wget


def create_directory(directory_name):
    """
    Description: This function create a directory named as parameter 'directory_name'.
    :param directory_name: Used to name the future directory.
    :return locate: The localisation of directory created. It will be captured in a variable for be used by
    fieldnames_csv(), create_csv(), connect_url_book() and scrap_write().
    """
    if os.path.exists(directory_name):
        shutil.rmtree(directory_name)
        os.mkdir(directory_name)
    else:
        os.mkdir(directory_name)
    locate = os.path.join('.', directory_name)
    return locate


locate_csv = create_directory('bts_csv')
locate_images = create_directory('images_bts')


def create_urlcatlist(number_category):
    """
    Description: This function create a list of all urls for a category.
    :param number_category: Is total number of categories + 3.
    :return exturlcatlist: This list contain all url categories without 'index.html'. It will be used by url_to_csv() as
    variable named urlcatlist.
    """
    url = 'http://books.toscrape.com/index.html'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'xml')
    i = 3
    exturlcatlist = []
    while i < number_category:
        midurlcat = soup.select('a')[i]['href'].replace('index.html', '')
        urlcat = 'http://books.toscrape.com/{}'.format(midurlcat)
        exturlcatlist.append(urlcat)
        i += 1
    return exturlcatlist


urlcatlist = create_urlcatlist(53)


def create_csv(soup, loctcsv, encode):
    """
    Description: This function collect all prerequisite for fieldnames().
    :param soup: soup = BeautifulSoup(r.text, 'xml'). r is a variable assign just before create_csv() is executed.
    :param loctcsv: The localisation of 'books_to_scrape_csv' is needed. 'books_to_scrape_csv' is a default name of a
    directory created by create_directory() which will contain all .csv.
    :param encode: For Unix is 'latin-1', for windows is 'utf-8'.
    """
    csvname = soup.select('h1')[0].string
    fieldnames_csv(loctcsv, csvname, encode)


def return_tag(soup):
    """
    Description: This function will return tag1. tag1 = number of books on a specific page (soup).
    :param soup: soup = BeautifulSoup(r.text, 'xml'). r is a variable assign just before return_tag() is executed.
    :return: 'tag1' is an integer. Tag1 = number of books in one page of a category.
    """
    linkbook = soup.select('h3 a')
    tag1 = len(linkbook)
    return tag1


def fieldnames_csv(loctcsv, csvname, encode):
    """
    Description: This function is executed in create_csv(). It will create an empty .csv in "books_to_scrape" using
    "category" as name.
    It determine also the fieldnames.
    :param loctcsv: Variable locate_csv from creatdirect()
    :param csvname: Variable csvname from "csvname = soup.select('h1')[0].string" executed just before this function.
    :param encode: For Unix is 'latin-1', for windows is 'utf-8'.
    "csvname" collect the name of the category.
    """
    name = os.path.join(loctcsv, csvname)
    with open('{}{}'.format(name, '_bts.csv'), 'a', newline='', encoding=encode) as new_file:
        fieldnames = ['product_page_url', 'upc', 'title', 'price_including_tax', 'price_excluding_tax',
                      'number_available', 'product_description', 'review_rating', 'image_url', 'image']
        writer = csv.DictWriter(new_file, fieldnames=fieldnames)
        writer.writeheader()


def scrap_write(url, loctcsv, image, soup, encode):
    """
    Description: This function collect all information needed and write it in its .csv in function of categories.
    :param url: Url of the book is needed.
    :param loctcsv: locate_csv
    :param image: Variable "image" is collect just before this function is executed.
    :param soup: "soup" is the parsing answer of r=requests.get(url).
    :param encode: For Unix is 'latin-1', for windows is 'utf-8'.
    """
    product_page_url = url
    title = soup.select("h1")[0].string
    upc = soup.select('table')[0].select('td')[0].string
    price_including_tax = soup.select('table')[0].select('td')[3].string
    price_excluding_tax = soup.select('table')[0].select('td')[2].string
    number_available = soup.select('table')[0].select('td')[5].string.replace('In stock (', '').replace('available)',
                                                                                                        '')
    category = soup.select('a')[3].text
    review_rating = soup.select('table')[0].select('td')[6].string
    image_url = (soup.select("img")[0]["src"]).replace('../../', "http://books.toscrape.com/")
    product_description = (soup.select("meta")[2]["content"]).replace('     ', '')

    name = os.path.join(loctcsv, category)
    with open('{}{}'.format(name, '_bts.csv'), 'r', encoding=encode) as csv_file:
        reader = csv.reader(csv_file)
        for header in reader:
            break

    with open('{}{}'.format(name, '_bts.csv'), 'a', newline='', encoding=encode) as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=header)
        writer.writerow({'product_page_url': product_page_url, 'upc': upc, 'title': title,
                         'price_including_tax': price_including_tax, 'price_excluding_tax': price_excluding_tax,
                         'number_available': number_available, 'product_description': product_description,
                         'review_rating': review_rating, 'image_url': image_url, 'image': image})
        csv_file.write("\n")


def connect_url_book(listurlbks, locimgs, loccsv, encode):
    """
    Description: For all urls in listurlbooks this function will make a request and use BeautifulSoup to download image
    with wget and collect all information needed with scrape_write().
    :param listurlbks: list of all url books of a category, Default named as urlcatlist.
    :param locimgs: Localisation of directory to redirect download images of books,
    Directory default named 'images_from_books_to_scrape'
    :param loccsv: Localisation of directory needed for opening right .csv in function of the category of the book.
    Directory default named 'books_to_scrape_csv'
    :param encode: For Unix is 'latin-1', for windows is 'utf-8'.
    """
    for elements in listurlbks:
        url = elements
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'xml')
        image_url = (soup.select("img")[0]["src"]).replace('../../', "http://books.toscrape.com/")
        image = wget.download(image_url, locimgs)
        scrap_write(url, loccsv, image, soup, encode)


def append_listurlbks(tag, soup, listurlbks, i):
    """
    Description: This function append Listurlbooks with all books of a category.
    :param tag: Tag is number of tag 'h3 a' in a category_page-n url . Tag = number of books in this page.
    :param soup: BeautifulSoup(requests_url_category_page_n.text, 'xml')
    :param listurlbks: All pages urls of a category will be append in that list.
    :param i: This variable is iterate for all books in a category.
    """
    for x in range(tag):
        urlbook = (soup.select('h3 a')[i]['href']).replace('../../../', 'http://books.toscrape.com/catalogue/')
        listurlbks.append(urlbook)
        i += 1


def url_to_csv(encode):
    """
    Description: This function will use "urlcatlist" to make a list of url's books named "listurlbooks".
    "If" is executed if the category has more than one page, "Else" is for others.
    Then it'll search, for each books of a category, information required and write it on its csv file(scrap_write()).
    """
    for urlcategory in urlcatlist:
        j = 1
        k = str(j)
        url = '{}{}{}{}'.format(urlcategory, 'page-', k, '.html')
        r = requests.get(url)
        if r:
            soup = BeautifulSoup(r.text, 'xml')
            create_csv(soup, locate_csv, encode)
            listurlbooks = []
            i = 0
            while r:
                soup = BeautifulSoup(r.text, 'xml')
                tag = return_tag(soup)
                append_listurlbks(tag, soup, listurlbooks, i)
                j += 1
                k = str(j)
                url = '{}{}{}{}'.format(urlcategory, 'page-', k, '.html')
                r = requests.get(url)
            connect_url_book(listurlbooks, locate_images, locate_csv, encode)
        else:
            url = '{}{}'.format(urlcategory, 'index.html')
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'xml')
            create_csv(soup, locate_csv, encode)
            i = 0
            listurlbooks = []
            tag = return_tag(soup)
            append_listurlbks(tag, soup, listurlbooks, i)
            connect_url_book(listurlbooks, locate_images, locate_csv, encode)


def main(encode):
    """
    Description: This function call all others in the following order; create_directories();
    create_urlcatlist(number_category) and url_to_csv(encode).
    :param encode: For Unix is 'latin-1' , For WINDOWS is 'utf-8'.
    """
    create_directory('bts_csv')
    create_directory('images_bts')
    create_urlcatlist(53)
    url_to_csv(encode)


# In main(encode) parameter by Default is 'latin-1'.
# Change it in function of your OS ; For Unix is 'latin-1' , For WINDOWS is 'utf-8'.
main('latin-1')
