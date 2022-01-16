from django.contrib import admin

# Register your models here.
from api.models import Note, Store

admin.site.register(Note)
admin.site.register(Store)
