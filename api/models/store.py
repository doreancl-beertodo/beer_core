from django.db import models

from storescraper.storescraper.utils import get_store_class_by_name


class Store(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField()

    scraper = property(
        lambda self: get_store_class_by_name("Ripley"))

    def update_pricing(self, ):
        scraper = self.scraper
        scraped_products_data = scraper.products(
            ['Notebook']
        )

        print(scraped_products_data)
        return [1, 2, 3]
