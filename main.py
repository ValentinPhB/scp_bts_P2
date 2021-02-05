# -*- coding: utf-8 -*-

import requests
import csv
from bs4 import BeautifulSoup

# Création d'une list des urls des catégories et scrapping nom catégories :

def exturlcat():

    url = 'http://books.toscrape.com/index.html'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'xml')
    i = 3
    urlcatlist = []
    while i < 53:
        midurlcat = soup.select('a')[i]['href'].replace('index.html', '')
        urlcat = 'http://books.toscrape.com/' + midurlcat
        urlcatlist.append(urlcat)
        i += 1
    return urlcatlist

urlcatlistvar = exturlcat()

# Création d'un fichier csv vide par catégorie :

def createcsv(category):

        with open(category + '_bts.csv', 'a', newline='') as new_file:
            fieldnames = ['product_page_url', 'upc', 'title', 'price_including_tax', 'price_excluding_tax',
                          'number_available', 'product_description', 'review_rating', 'image_url']
            writer = csv.DictWriter(new_file, fieldnames=fieldnames)
            writer.writeheader()

# Fonction pour rechercher et renvoyer informations voulues  :

def search(soup, url):

    product_page_url = url
    title = soup.select("h1")[0].string
    upc = soup.select('table')[0].select('td')[0].string
    price_including_tax = soup.select('table')[0].select('td')[3].string.replace('Â', '')
    price_excluding_tax = soup.select('table')[0].select('td')[2].string.replace('Â', '')
    number_available = soup.select('table')[0].select('td')[5].string.replace('In stock (', '').replace('available)',
                                                                                                        '')
    category = soup.select('a')[3].text
    review_rating = soup.select('table')[0].select('td')[6].string
    image_url = (soup.select("img")[0]["src"]).replace('../../', "http://books.toscrape.com/")
    product_description = (soup.select("meta")[2]["content"]).replace('     ', '')
    return (product_page_url,upc,title,price_including_tax,price_excluding_tax,number_available,product_description,
            category,review_rating,image_url)

# Fonction pour écrire informations voulues dans fichier csv nommé comme catégorie :

def writecsv(product_page_url, upc, title, price_including_tax, price_excluding_tax, number_available,
             product_description, category, review_rating, image_url):

        with open(category + '_bts.csv', 'r') as csv_file:
            reader = csv.reader(csv_file)
            for header in reader:
                break

        with open(category + '_bts.csv', 'a', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=header)
            writer.writerow({'product_page_url': product_page_url, 'upc': upc, 'title': title,
                                 'price_including_tax': price_including_tax, 'price_excluding_tax': price_excluding_tax,
                                 'number_available': number_available, 'product_description': product_description,
                                 'review_rating': review_rating, 'image_url': image_url})
            csv_file.write("\n")

# Création d'une liste des urls des livres par catégories, + search(), + writecsv() :

def listurlbooks():

    for urlcategory in urlcatlistvar:
        j = 1
        k = str(j)
        url = urlcategory + 'page-' + k + '.html'
        r = requests.get(url)
        if r:
            listurlbooks = []
            while r:
                soup = BeautifulSoup(r.text, 'xml')
                linkbook = soup.select('h3 a')
                l = 0
                for elements in linkbook:
                    urlbook = (soup.select('h3 a')[l]['href']).replace('../../../',
                                                                       'http://books.toscrape.com/catalogue/')
                    listurlbooks.append(urlbook)
                    l += 1
                k = int(j)
                j += 1
                k = str(j)
                url = urlcategory + 'page-' + k + '.html'
                r = requests.get(url)
            for elements in listurlbooks:
                url = elements
                r = requests.get(url)
                soup = BeautifulSoup(r.text, 'xml')
                search(soup, url)
                product_page_url = search(soup, url)[0]
                upc = search(soup, url)[1]
                title = search(soup, url)[2]
                price_including_tax = search(soup, url)[3]
                price_excluding_tax = search(soup, url)[4]
                number_available = search(soup, url)[5]
                product_description = search(soup, url)[6]
                category = search(soup, url)[7]
                review_rating = search(soup, url)[8]
                image_url = search(soup, url)[9]
                createcsv(category)
                writecsv(product_page_url, upc, title, price_including_tax, price_excluding_tax, number_available,
                         product_description, category, review_rating, image_url)
        else:
            listurlbooks = []
            url = urlcategory + 'index.html'
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'xml')
            linkbook = soup.select('h3 a')
            l = 0
            for elements in linkbook:
                urlbook = (soup.select('h3 a')[l]['href']).replace('../../../', 'http://books.toscrape.com/catalogue/')
                listurlbooks.append(urlbook)
                l += 1
            for elements in listurlbooks:
                url = elements
                r = requests.get(url)
                soup = BeautifulSoup(r.text, 'xml')
                search(soup, url)
                product_page_url = search(soup, url)[0]
                upc = search(soup, url)[1]
                title = search(soup, url)[2]
                price_including_tax = search(soup, url)[3]
                price_excluding_tax = search(soup, url)[4]
                number_available = search(soup, url)[5]
                product_description = search(soup, url)[6]
                category = search(soup, url)[7]
                review_rating = search(soup, url)[8]
                image_url = search(soup, url)[9]
                createcsv(category)
                writecsv(product_page_url, upc, title, price_including_tax, price_excluding_tax, number_available,
                         product_description, category, review_rating, image_url)


def main():

    exturlcat()
    listurlbooks()


main()


