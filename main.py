#!/usr/bin/env python

from bs4 import BeautifulSoup
import csv
import requests
import os
import shutil
import wget


def create_directories():
    """
    Description: This function create two directories ("books_to_scrape" for .csv and "images_books_to_scrape"
    for images).It also delete older versions of this directories.
    :return: locate_csvfc and locate_imagesfc.They are captured in locate_csv and locate_images variables respectively .
    """
    if os.path.exists('books_to_scrape'):
        shutil.rmtree('books_to_scrape')
        os.mkdir('books_to_scrape')
    else:
        os.mkdir('books_to_scrape')
    locate_csvfc = os.path.join('.', 'books_to_scrape')

    if os.path.exists('images_books_to_scrape'):
        shutil.rmtree('images_books_to_scrape')
        os.mkdir('images_books_to_scrape')
    else:
        os.mkdir('images_books_to_scrape')
    locate_imagesfc = os.path.join('.', 'images_books_to_scrape')

    return locate_csvfc, locate_imagesfc


locate_csv = create_directories()[0]
locate_images = create_directories()[1]


def create_urlcatlist(number_category):
    """
    Description: This function create a list of all url's categories from the site "Books to scrape".
    :param number_category: Is total number of categories + 3.
    :return: it return list "exturlcatlist" that will be captured in "urlcatlist" variable.
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


def create_csv(loccsv, csvname):
    """
    Description: This function create an empty .csv in "books_to_scrape" using "category" as name.
    It determine also the fieldnames.
    :param loccsv: Variable locate_csv from creatdirect()
    :param csvname: Variable csvname from "csvname = soup.select('h1')[0].string" executed just before this function.
    "csvname" collect the name of the category.
    """
    name = os.path.join(loccsv, csvname)
    with open('{}{}'.format(name, '_bts.csv'), 'a', newline='', encoding='latin-1') as new_file:
        fieldnames = ['product_page_url', 'upc', 'title', 'price_including_tax', 'price_excluding_tax',
                      'number_available', 'product_description', 'review_rating', 'image_url', 'image']
        writer = csv.DictWriter(new_file, fieldnames=fieldnames)
        writer.writeheader()


def scrap_write(url, loccsv, image, soup):
    """
    Description: This function collect all information needed and write it in its .csv in function of categories.
    :param url: Url of the book is needed.
    :param loccsv: locate_csv
    :param image: Variable "image" is collect just before this function is executed.
    :param soup: "soup" is the parsing answer of r=requests.get(url).
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

    name = os.path.join(loccsv, category)
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


def url_to_csv():
    """
    Description: This function will use "urlcatlist" to make a list of url's books named "listurlbooks".
    "If" is executed if the category has more than one page.
    "Else" is for others.
    Then it'll search, for each books of a category, information required and write it on its csv file(scrap_write()).
    """
    for urlcategory in urlcatlist:
        j = 1
        k = str(j)
        url = '{}{}{}{}'.format(urlcategory, 'page-', k, '.html')
        r = requests.get(url)
        if r:
            soup = BeautifulSoup(r.text, 'xml')
            csvname = soup.select('h1')[0].string
            create_csv(locate_csv, csvname)
            listurlbooks = []
            while r:
                soup = BeautifulSoup(r.text, 'xml')
                linkbook = soup.select('h3 a')
                tag = len(linkbook)
                i = 0
                for x in range(tag):
                    urlbook = (soup.select('h3 a')[i]['href']).replace('../../../',
                                                                       'http://books.toscrape.com/catalogue/')
                    listurlbooks.append(urlbook)
                    i += 1
                j += 1
                k = str(j)
                url = '{}{}{}{}'.format(urlcategory, 'page-', k, '.html')
                r = requests.get(url)
            for elements in listurlbooks:
                url = elements
                r = requests.get(url)
                soup = BeautifulSoup(r.text, 'xml')
                image_url = (soup.select("img")[0]["src"]).replace('../../', "http://books.toscrape.com/")
                image = wget.download(image_url, locate_images)
                scrap_write(url, locate_csv, image, soup)

        else:
            listurlbooks = []
            url = '{}{}'.format(urlcategory, 'index.html')
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'xml')
            csvname = soup.select('h1')[0].string
            create_csv(locate_csv, csvname)
            linkbook = soup.select('h3 a')
            tag = len(linkbook)
            i = 0
            for x in range(tag):
                urlbook = (soup.select('h3 a')[i]['href']).replace('../../../', 'http://books.toscrape.com/catalogue/')
                listurlbooks.append(urlbook)
                i += 1
            for elements in listurlbooks:
                url = elements
                r = requests.get(url)
                soup = BeautifulSoup(r.text, 'xml')
                image_url = (soup.select("img")[0]["src"]).replace('../../', "http://books.toscrape.com/")
                image = wget.download(image_url, locate_images)
                scrap_write(url, locate_csv, image, soup)


def main():
    """
    Description: This function call all others in the following order; create_directories();
     create_urlcatlist(number_category) and url_to_csv().
    """
    create_directories()
    create_urlcatlist(53)
    url_to_csv()


main()
