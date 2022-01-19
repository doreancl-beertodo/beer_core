from django.contrib import admin

# Register your models here.
from api.models import Note, Store, Country, StoreType

admin.site.register(Note)
admin.site.register(Store)
admin.site.register(Country)
admin.site.register(StoreType)
