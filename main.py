#!/usr/bin/env python

from bs4 import BeautifulSoup
import os
import pandas as pd
from progress.bar import IncrementalBar
import requests
import shutil
import urllib.request


def create_directory(directory_name):
    """
    Description: This function create a directory named as 'directory_name'.
    :param directory_name: This parameter is used to name the future directory.
    :return path: "path" is the localisation of directory created. Default named "path_csv" for future .csv and
    "path_images" for images.
    """
    if os.path.exists(directory_name):
        shutil.rmtree(directory_name)
        os.mkdir(directory_name)
    else:
        os.mkdir(directory_name)
    path = os.path.join('.', directory_name)
    return path


def extract_category_list():
    """
    Description: This function extract all categories URLs.
    :return: "extract_url" as a list. It contain all categories URLs without "index.html". They will be tested by
    extract_books_url(first_step). "extract_url" is default named "step_1" from main().
    """
    url = 'http://books.toscrape.com/index.html'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'xml')
    step_one = soup.aside.li.select('a', href=True)
    url_categories = []

    for a in step_one:
        if a.text:
            step_two = 'http://books.toscrape.com/{}'.format(a['href'].replace('index.html', ''))
            url_categories .append(step_two)
    del url_categories[0]
    return url_categories


def create_books_url_list(rep, list_url):
    """
    Description: This function will add all books URLs from a category in "list_url".
    :param rep: This parameter is a variable named 'r' from this function.
    :param list_url: This parameter is "List_books" from this function.
    :return: list_books will be returned with all URLs.
    """
    soup = BeautifulSoup(rep.text, 'xml')
    link_book = soup.select('h3 a')
    tag = len(link_book)
    k = 0
    for x in range(tag):
        url_book = (soup.select('h3 a')[k]['href']).replace('../../../', 'http://books.toscrape.com/catalogue/')
        list_url.append(url_book)
        k += 1
    return list_url


def extract_books_url(first_step):
    """
    Description: This function will test all URLs contained in step_1 to know if category contains more than one page
    (more than 20 books).
    :param first_step: This parameter is returned by extract_category_list(). Default named "step_1" from main().
    :return: "list_books" as a list. It contains all urls books of first_step[0]. Default named "step_2" from main().
    """
    if first_step[0]:
        j = 1
        number_page = str(j)
        url = '{}{}{}{}'.format(first_step[0], 'page-', number_page, '.html')
        r = requests.get(url)
        list_books = []
        if r:
            while r:
                list_books = create_books_url_list(r, list_books)
                j += 1
                number_page = str(j)
                url = '{}{}{}{}'.format(first_step[0], 'page-', number_page, '.html')
                r = requests.get(url)
        else:
            url = '{}{}'.format(first_step[0], 'index.html')
            r = requests.get(url)
            list_books = create_books_url_list(r, list_books)
        return list_books


def transform_books_information(second_step, loc_images):
    """
    Description: This function will transform all information extracted and capture them in lists.
    :param second_step: This parameter is returned by extract_books_url(first_step). Default named "step_2" from main().
    :param loc_images: This parameter is returned by create_directory(directory_name).
    Default named "path_images" from main().
    :return: "data" as a dictionary. It contain all lists as items. Default named "step_3" from main().
    """
    product_page_url = []
    title = []
    upc = []
    price_including_tax = []
    price_excluding_tax = []
    number_available = []
    category = []
    review_rating = []
    image_url = []
    product_description = []
    image_loc = []

    for element in second_step:
        r = requests.get(element)
        soup = BeautifulSoup(r.text, 'xml')

        product_page_url.append('=HYPERLINK("{}")'.format(element))

        upc.append(soup.select('table')[0].select('td')[0].string)

        title_bk2 = soup.select("h1")[0].string.replace('/', '_')
        title_bk = '{}{}'.format(title_bk2, '.jpg')
        title.append(soup.select("h1")[0].string)

        price_including_tax.append(soup.select('table')[0].select('td')[3].string)

        price_excluding_tax.append(soup.select('table')[0].select('td')[2].string)

        number_available.append(soup.select('table')[0].select('td')[5].string.replace('In stock (',
                                                                                       '').replace('available)', ''))
        product_description.append((soup.select("meta")[2]["content"]).replace('     ', ''))

        category.append(soup.select('a')[3].text)

        review_rating.append(soup.select('p')[2]['class'].replace('star-rating ', ''))

        image_url_variable = ((soup.select("img")[0]["src"]).replace('../../', "http://books.toscrape.com/"))
        image_url.append('=HYPERLINK("{}")'.format(image_url_variable))
        image_file = os.path.join(loc_images, title_bk)
        urllib.request.urlretrieve(image_url_variable, image_file)

        image_loc.append(image_file)

    data = {"product_page_url": product_page_url, "title": title, "upc": upc,
            "price_including_tax": price_including_tax, "price_excluding_tax": price_excluding_tax, "number_available":
            number_available, "category": category, "review_rating": review_rating, "image_url": image_url,
            "product_description": product_description, "image_loc": image_loc}

    return data


def load_books_information(dictionary, loc_csv):
    """
    Description: This function will load all information contained in "dictionary" to .csv and name it as category name.
    :param dictionary: This parameter is returned by transform_books_information(second_step, loc_images).
    Default named "step_3" from main().
    :param loc_csv: This parameter is returned by create_directory(directory_name).
    Default named "path_csv" from main().
    """
    category = dictionary["category"][0]
    csv_name = '{}{}'.format(category, '.csv')
    path = os.path.join(loc_csv, csv_name)

    data_frame = pd.DataFrame.from_dict(dictionary)
    data_frame.to_csv(path_or_buf=path, sep=',', na_rep='No information', encoding='latin-1')


def main():
    """
    Description: This function call all others in the right following order.
    """
    path_csv = create_directory('bts_csv')
    path_images = create_directory('images_bts')

    step_1 = extract_category_list()

    # Initialization of Progress Bar
    bar = IncrementalBar('Progression', max=len(step_1))
    bar.start()

    while step_1 is not []:
        if not step_1:
            break
        else:
            step_2 = extract_books_url(step_1)
            step_3 = transform_books_information(step_2, path_images)
            load_books_information(step_3, path_csv)
            del step_1[0]

            # Progress Bar incrementation :
            bar.next()


main()
