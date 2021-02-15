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
    :param directory_name: This parameter is used to name the future directory.
    :return locate: This parameter is the localisation of directory created. It will be captured in a variable
    for be used by fieldnames_csv(), create_csv(), connect_url_book() and scrap_write().
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
    :param number_category: This parameter is total number of categories + 3.
    :return exturlcatlist: This parameter is a list. It contain all url categories without 'index.html'.
    It will be used by url_to_csv() as a variable named urlcatlist.
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


def create_csv(soup, loctcsv):
    """
    Description: This function collect prerequisite for fieldnames().
    :param soup: This parameter refer to variable named 'soup' assign right before this function is executed.
    :param loctcsv:  This parameter is locate_csv from create_directory().
    """
    csvname = soup.select('h1')[0].string
    fieldnames_csv(loctcsv, csvname)


def return_tag(soup):
    """
    Description: This function will return tag1. tag1 = number of books on a specific page (soup).
    :param soup: This parameter refer to variable named 'soup' assign right before this function is executed.
    :return: 'tag1' is an integer. Tag1 = number of books in one page of a category.
    """
    linkbook = soup.select('h3 a')
    tag1 = len(linkbook)
    return tag1


def fieldnames_csv(loctcsv, csvname):
    """
    Description: This function is executed in create_csv(). It will create an empty .csv in "books_to_scrape" using
    "category" as name.
    It determine also the fieldnames.
    :param loctcsv:  This parameter is locate_csv from create_directory().
    :param csvname: This parameter is csvname from "csvname = soup.select('h1')[0].string" executed just before
    this function.
    """
    name = os.path.join(loctcsv, csvname)
    with open('{}{}'.format(name, '_bts.csv'), 'a', newline='', encoding='latin-1') as new_file:
        fieldnames = ['product_page_url', 'upc', 'title', 'price_including_tax', 'price_excluding_tax',
                      'number_available', 'product_description', 'review_rating', 'image_url', 'image']
        writer = csv.DictWriter(new_file, fieldnames=fieldnames)
        writer.writeheader()


def scrap_write(url, loctcsv, image, soup):
    """
    Description: This function collect all information needed and write it in its .csv.
    :param url: This parameter is url of the book.
    :param loctcsv: This parameter is locate_csv from create_directory().
    :param image: This parameter is variable "image". It's collect just before this function is executed.
    :param soup: This parameter refer to variable named 'soup' assign right before this function is executed.
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
    with open('{}{}'.format(name, '_bts.csv'), 'r', encoding='latin-1') as csv_file:
        reader = csv.reader(csv_file)
        for header in reader:
            break

    with open('{}{}'.format(name, '_bts.csv'), 'a', newline='', encoding='latin-1') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=header)
        writer.writerow({'product_page_url': product_page_url, 'upc': upc, 'title': title,
                         'price_including_tax': price_including_tax, 'price_excluding_tax': price_excluding_tax,
                         'number_available': number_available, 'product_description': product_description,
                         'review_rating': review_rating, 'image_url': image_url, 'image': image})
        csv_file.write("\n")


def connect_url_book(listurlbks, locimgs, loccsv):
    """
    Description: For all urls in listurlbooks this function will make a request and use BeautifulSoup to download image
    with wget and collect all information needed with scrape_write().
    :param listurlbks: This parameter is a list. It contain all url books of a category, Default named as urlcatlist.
    :param locimgs: This parameter is 'images_bts' from create_directory().
    :param loccsv: This parameter is locate_csv from create_directory().
    """
    for elements in listurlbks:
        url = elements
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'xml')
        image_url = (soup.select("img")[0]["src"]).replace('../../', "http://books.toscrape.com/")
        image = wget.download(image_url, locimgs)
        scrap_write(url, loccsv, image, soup)


def append_listurlbks(tag, soup, listurlbks, i):
    """
    Description: This function append Listurlbooks with all books of a category.
    :param tag: This parameter is number of tag 'h3 a' in a category_page-n url. Tag = number of books in this page.
    :param soup: This parameter refer to variable named 'soup' assign right before this function is executed.
    :param listurlbks: This parameter is a list. Default named as urlcatlist.
    :param i: This parameter is a variable.Its iterate for all books in a category.
    """
    for x in range(tag):
        urlbook = (soup.select('h3 a')[i]['href']).replace('../../../', 'http://books.toscrape.com/catalogue/')
        listurlbks.append(urlbook)
        i += 1


def url_to_csv():
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
            create_csv(soup, locate_csv)
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
            connect_url_book(listurlbooks, locate_images, locate_csv)
        else:
            url = '{}{}'.format(urlcategory, 'index.html')
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'xml')
            create_csv(soup, locate_csv)
            i = 0
            listurlbooks = []
            tag = return_tag(soup)
            append_listurlbks(tag, soup, listurlbooks, i)
            connect_url_book(listurlbooks, locate_images, locate_csv)


def main():
    """
    Description: This function call all others in the right following order.
    """
    create_directory('bts_csv')
    create_directory('images_bts')
    create_urlcatlist(53)
    url_to_csv()


main()
