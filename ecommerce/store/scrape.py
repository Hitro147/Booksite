from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

from .models import Product
import django
django.setup()

my_urls = ['https://www.barnesandnoble.com/b/books/_/N-1fZ29Z8q8?Nrpp=20&page=1',
           'https://www.barnesandnoble.com/b/books/_/N-1fZ29Z8q8?Nrpp=20&page=2',
           'https://www.barnesandnoble.com/b/books/_/N-1fZ29Z8q8?Nrpp=20&page=3',
           'https://www.barnesandnoble.com/b/books/_/N-1fZ29Z8q8?Nrpp=20&page=4',
           'https://www.barnesandnoble.com/b/books/_/N-1fZ29Z8q8?Nrpp=20&page=5',
           ]

# opening up connection and grabbing the page
for url in my_urls:
    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()

    # html parsing

    page_soup = soup(page_html, 'html.parser')

    # grabs each product

    containers = page_soup.findAll('div', {'class': 'row topX-row'})

    for container in containers:
        img = container.a.img['src']

        title_container = container.findAll('h3', {'class': 'product-info-title'})
        title = title_container[0].text[1:-14]

        price_container = container.findAll('span', {'class': 'current'})
        price = float(price_container[0].text[2:])

        author_container = container.findAll('div', {'class': 'product-shelf-author contributors'})
        author = author_container[0].text

        object = Product.objects.create(name=title, price=price, image=img, author = author)
        object.save()

        # len_of_price = len(price)//2

        print('image url:', img)
        print('title:', title)
        print('price:', price)
        print('author:', author)
