import json
from decimal import Decimal

from bs4 import BeautifulSoup

from storescraper.storescraper.product import Product
from storescraper.storescraper.store import Store
from storescraper.storescraper.utils import session_with_proxy


class Ripley(Store):
    preferred_products_for_url_concurrency = 3

    @classmethod
    def products_for_url(cls, url, category=None, extra_args=None):
        # This implementation of products_for_url is botched to obtain the
        # products directly from the PLP page of Ripley because we can't
        # make too many requests to the Ripley website. Therefore "url" is
        # just the name of the category and ignored

        # This method may be called as part of the keyword search functionality
        # of the library. We patch it by detecting this call and calling
        # a function that actually uses the URL PDP page of the product.
        if extra_args and extra_args.get('source', None) == 'keyword_search':
            return [cls._assemble_full_product(
                url, category, extra_args)]

        category_paths = [
            ['tecno/computacion/notebooks', ['Notebook'], 'Tecno > Computación > Notebooks', 1],
            #['tecno/computacion/notebooks-gamer', ['Notebook'], 'Tecno > Computación > Notebooks gamer', 1],
        ]

        session = session_with_proxy(extra_args)

        if extra_args and 'user-agent' in extra_args:
            session.headers['user-agent'] = extra_args['user-agent']

        fast_mode = extra_args.get('fast_mode', True)
        print('fast_mode', fast_mode)

        url_base = 'https://simple.ripley.cl/{}?page={}'
        product_dict = {}

        for e in category_paths:
            category_path, local_categories, section_name, category_weight = e

            if category not in local_categories:
                continue

            page = 1
            position = 1

            while True:
                if page > 200:
                    raise Exception('Page overflow')

                category_url = url_base.format(category_path, page)
                print(category_url)
                response = session.get(category_url, allow_redirects=False)

                if response.status_code != 200 and page == 1:
                    raise Exception('Invalid section: ' + category_url)

                soup = BeautifulSoup(response.text, 'html.parser')
                products_data = soup.find('script',
                                          {'type': 'application/ld+json'})

                products_soup = soup.find('div', 'catalog-container')

                if not products_data or not products_soup:
                    if page == 1:
                        logging.warning('Empty path: {}'.format(category_url))
                    break

                products_elements = products_soup.findAll(
                    'div', 'ProductItem__Row')

                if not products_elements:
                    products_elements = products_soup.findAll(
                        'a', 'catalog-product-item')

                products_json = json.loads(products_data.text)[
                    'itemListElement']

                assert (len(products_elements) == len(products_json))

                for product_json in products_json:
                    product_element = products_elements[
                        int(product_json['position']) - 1]
                    product_data = product_json['item']

                    brand = product_data.get('brand', '').upper()

                    if brand in ['LG', 'SAMSUNG'] and 'MPM' not in \
                            product_data['sku'] and not fast_mode:
                        # If the product is LG or Samsung and is sold directly
                        # by Ripley (not marketplace) obtain the full data

                        product = product_dict.get(product_data['sku'], None)
                        if not product:
                            url = cls._get_entry_url(product_element)
                            product = cls._assemble_full_product(
                                url, category, extra_args)
                    elif category == 'Headphones' and 'MPM' in \
                            product_data['sku']:
                        # Skip the thousands of headphones sold in marketplace
                        continue
                    else:
                        product = cls._assemble_product(
                            product_data, product_element, category)

                    if product:
                        if product.sku in product_dict:
                            product_to_update = product_dict[product.sku]
                        else:
                            product_dict[product.sku] = product
                            product_to_update = product

                        product_to_update.positions[section_name] = position

                    position += 1

                if fast_mode and page >= 1:
                    break

                page += 1

        products_list = [p for p in product_dict.values()]

        return products_list

    @classmethod
    def _assemble_product(cls, data, element, category):
        # Element Data (Varies by page)
        if element.name == 'div':
            element_name = element.find(
                'a', 'ProductItem__Name').text.replace('  ', ' ').strip()
        else:
            element_name = element.find(
                'div', 'catalog-product-details__name') \
                .text.replace('  ', ' ').strip()

        # Common

        # This is removing extra white spaces in between words
        # If not done, sometimes it will not be equal to element name
        data_name = " ".join([a for a in data['name'].split(' ') if a != '']) \
            .strip()

        assert (element_name == data_name)

        # Remove weird characters, e.g.
        # https://simple.ripley.cl/tv-portatil-7-negro-mpm00003032468
        name = data_name.encode('ascii', 'ignore').decode('ascii')
        sku = data['sku']
        url = cls._get_entry_url(element)

        if 'image' in data:
            picture_urls = ['https:{}'.format(data['image'])]
        else:
            picture_urls = None

        if data['offers']['price'] == 'undefined':
            return None

        offer_price = Decimal(data['offers']['price'])
        normal_price_container = element.find(
            'li', 'catalog-prices__offer-price')

        if normal_price_container:
            normal_price = Decimal(
                element.find('li', 'catalog-prices__offer-price')
                    .text.replace('$', '').replace('.', ''))
        else:
            normal_price = offer_price

        if normal_price < offer_price:
            offer_price = normal_price

        stock = 0
        if data['offers']['availability'] == 'http://schema.org/InStock':
            stock = -1

        if '-mpm' in url:
            seller = 'External seller'
        else:
            seller = None

        p = Product(
            name,
            cls.__name__,
            category,
            url,
            url,
            sku,
            stock,
            normal_price,
            offer_price,
            'CLP',
            sku=sku,
            picture_urls=picture_urls,
            seller=seller
        )

        return p

    @classmethod
    def _get_entry_url(cls, element):
        # Element Data (Varies by page)
        if element.name == 'div':
            url_extension = element.find('a')['href']
        else:
            url_extension = element['href']

        url = 'https://simple.ripley.cl{}'.format(url_extension)
        return url
