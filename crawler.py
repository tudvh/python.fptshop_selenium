from bs4 import BeautifulSoup
from selenium import webdriver
import random
import json

from product import Product


def create_chrome_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    return webdriver.Chrome(options=options)


def get_soup(url):
    browser = create_chrome_driver()
    browser.get(url)
    soup = BeautifulSoup(browser.page_source, 'html.parser')
    browser.quit()
    return soup


def write_log(title, content):
    with open('log.txt', 'a', encoding='utf-8') as f:
        f.seek(0, 2)
        f.write(f'{title}: {content}\n')


def get_product_detail(url, product: Product, num):
    if num == 0:
        write_log('Thất bại', product.name)
        return False

    try:
        soup = get_soup(url)

        product.set_brand_name(soup.select_one(
            'ol.breadcrumb.breadcrumb-margin li.active a').get('title'))
        product.set_price(soup.select_one(
            '.st-price-main').text.replace('₫', '').replace('.', ''))
        product.set_quantity(random.randint(10, 20))
        product.set_specs("".join([str(tr).replace("'", "\\'") for tr in soup.select(
            '.l-pd-body__right .card-body table tbody tr')]))
        product.set_description("".join([str(x).replace("'", "\\'") for x in soup.select(
            '.l-pd-body__left .card-body .st-pd-content > *')]))
        product.set_images([image.get('data-src').replace('images.fpt.shop/unsafe/fit-in/filters:quality(90):fill(white):upscale()/', '')
                            for image in soup.select('.st-slider .swiper-wrapper .swiper-slide')])

        return product
    except:
        write_log('Gọi lại', product.name)
        return get_product_detail(url, product, num-1)


def main():
    URL_LIST_PHONE = 'https://fptshop.com.vn/dien-thoai?hang-san-xuat=apple-iphone,samsung,oppo,xiaomi,realme,vivo&trang=4'
    URL_LIST_LAPTOP = 'https://fptshop.com.vn/may-tinh-xach-tay?hang-san-xuat=apple-macbook,asus,hp,acer,msi,dell&trang=4'
    URL_LIST_TABLET = 'https://fptshop.com.vn/may-tinh-bang?hang-san-xuat=apple-ipad,samsung,xiaomi,oppo&trang=4'

    list_products = []
    with open('data_crawled.txt', 'r', encoding='utf-8') as f:
        file_content = f.read()
        if file_content:
            list_products = json.loads(file_content)

    soup = get_soup(URL_LIST_PHONE)

    if list_products:
        url_last = list_products[-1]['url']
        selector = f'.cdt-product-wrapper > .cdt-product:has(a.cdt-product__name[href="{url_last}"]) ~ .cdt-product a.cdt-product__name'
        list_products_web = soup.select(selector)
    else:
        list_products_web = soup.select(
            '.cdt-product-wrapper > .cdt-product a.cdt-product__name')

    for product_web in list_products_web:
        product = Product()
        product.set_name(product_web['title'].replace("'", "\\'"))
        product.set_url(product_web["href"])

        product = get_product_detail(
            f'https://fptshop.com.vn{product.url}', product, 3)

        if not product:
            continue

        list_products.append(product.get_all())

        with open('sql.txt', 'w', encoding='utf-8') as f:
            json.dump(list_products, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
    main()
