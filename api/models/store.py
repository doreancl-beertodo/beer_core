from django.db import models
from sorl.thumbnail import ImageField

from storescraper.storescraper.utils import get_store_class_by_name
# from .country import Country
from ..utils import iterable_to_dict


class Store(models.Model):
    name = models.CharField(max_length=255, db_index=True, unique=True, null=True)
    # country = models.ForeignKey(Country, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    storescraper_class = models.CharField(max_length=255, db_index=True, null=True)
    storescraper_extra_args = models.CharField(max_length=255, null=True, blank=True)
    # type = models.ForeignKey(StoreType, on_delete=models.CASCADE)
    logo = ImageField(upload_to='store_logos', default='default.jpg')

    scraper = property(
        lambda self: get_store_class_by_name("Ripley"))

    def __str__(self):
        return self.name

    def update_pricing(self, ):
        scraper = self.scraper
        categories = ['Notebook']

        scraped_products_data = scraper.products(
            categories
        )

        print(scraped_products_data)

        scraped_products = scraped_products_data['products']

        discovery_urls_without_products = \
            scraped_products_data['discovery_urls_without_products']

        update_log = None
        self.update_with_scraped_products(categories, scraped_products,
                                          discovery_urls_without_products,
                                          update_log=update_log)

        return [1, 2, 3]

    def update_with_scraped_products(self, categories, scraped_products,
                                     discovery_urls_without_products,
                                     update_log=None):
        from api.models import Entity

        print(categories, scraped_products,
              discovery_urls_without_products,
              update_log)

        scraped_products_dict = iterable_to_dict(scraped_products, 'key')

        for scraped_product in scraped_products_dict.values():
            print(scraped_product)

            Entity.create_from_scraped_product(
                scraped_product,
                self,
                #categories_dict[scraped_product.category],
                #currencies_dict[scraped_product.currency],
            )
