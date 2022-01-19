from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from gtin_fields import fields as gtin_fields

from .store import Store


class Entity(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    # category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # scraped_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='+')
    # currency = models.ForeignKey(Currency, on_delete=models.CASCADE)
    condition = models.URLField(choices=[
        ('https://schema.org/DamagedCondition', 'Damaged'),
        ('https://schema.org/NewCondition', 'New'),
        ('https://schema.org/RefurbishedCondition', 'Refurbished'),
        ('https://schema.org/UsedCondition', 'Used')
    ])
    # product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    # cell_plan = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name='+')
    # active_registry = models.OneToOneField('EntityHistory',
    #                                       on_delete=models.CASCADE,
    #                                       related_name='+',
    #                                       null=True)
    name = models.CharField(max_length=256, db_index=True)
    cell_plan_name = models.CharField(max_length=50, null=True,
                                      blank=True, db_index=True)
    part_number = models.CharField(max_length=50, null=True, blank=True,
                                   db_index=True)
    sku = models.CharField(max_length=50, null=True, blank=True, db_index=True)
    ean = gtin_fields.EAN13Field(null=True, blank=True)
    key = models.CharField(max_length=256, db_index=True)
    url = models.URLField(max_length=512, db_index=True)
    discovery_url = models.URLField(max_length=512, db_index=True)
    picture_urls = models.TextField(blank=True, null=True)
    description = models.TextField(null=True)
    is_visible = models.BooleanField(default=True)

    # Metadata

    creation_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    # The last time the entity was associated. Important to leave standalone as
    # it is used for staff payments
    last_association = models.DateTimeField(null=True, blank=True)
    last_association_user = models.ForeignKey(get_user_model(),
                                              on_delete=models.CASCADE,
                                              null=True)

    # Last time a staff accessed the entity in the backend. Used to display a
    # warning to other staff if they try to access it at the same time.
    last_staff_access = models.DateTimeField(null=True, blank=True)
    last_staff_access_user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, null=True,
        related_name='+')

    # The last time the pricing of this entity was updated. Needed because
    # active_registry may be null. It does not match the active_registry date
    # either way because the registry uses the timestamp of the scraping, and
    # this field uses the timestamp of the moment it is updated in the database
    last_pricing_update = models.DateTimeField()

    def __str__(self):
        result = '{} - {}'.format(self.store, self.name)
        if self.cell_plan_name:
            result += ' / {}'.format(self.cell_plan_name)
        result += ' ({})'.format(self.category)

        return result

    @classmethod
    def create_from_scraped_product(cls, scraped_product, store):
        new_entity = cls.objects.create(
            store=store,
            # category=category,
            # scraped_category=category,
            # currency=currency,
            condition=scraped_product.condition,
            name=scraped_product.name,
            # cell_plan_name=scraped_product.cell_plan_name,
            part_number=scraped_product.part_number,
            sku=scraped_product.sku,
            ean=scraped_product.ean,
            key=scraped_product.key,
            url=scraped_product.url,
            discovery_url=scraped_product.discovery_url,
            picture_urls=scraped_product.picture_urls_as_json(),
            description=scraped_product.description,
            is_visible=True,
            last_pricing_update=timezone.now(),
        )

        new_entity.save()
