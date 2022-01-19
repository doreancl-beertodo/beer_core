from django.db import models
from sorl.thumbnail import ImageField

class Country(models.Model):
    name = models.CharField(max_length=200)
    iso_code = models.CharField(max_length=2)
    flag = ImageField(upload_to='country_flags')

    def __str__(self):
        return self.name

