from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from .models import Product
import django
django.setup()

my_url = 'https://www.amazon.in/b/ref=s9_acss_bw_ln_BXHPleft_1_2_w?node=7145567031&pf_rd_m=A1K21FY43GMZF8&pf_rd_s=merchandised-search-leftnav&pf_rd_r=2PH2YR8PNYG25NYQD9ZM&pf_rd_t=101&pf_rd_p=7603746b-fd2f-401f-af74-37cbf57e1014&pf_rd_i=976389031'

# opening up connection and grabbing the page

uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()

# html parsing

page_soup = soup(page_html, 'html.parser')

# grabs container

containers = page_soup.findAll('div', {'class':'a-section acs-product-block acs-product-block--default'})

for container in containers:
    img = container.a.img['src']

    title_container = container.findAll('span', {'class': 'a-truncate-full'})
    title = title_container[0].text

    price_container = container.findAll('span', {'class': 'a-price-whole'})
    try:
        price = float(price_container[0].text)
    except:
        price = 0.0

    object= Product.objects.create(name = title, price = price, image = img)
    object.save()

    #len_of_price = len(price)//2

    print('image url:', img)
    print('title:', title)
    print('price:', price)