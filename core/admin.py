from django.contrib import admin
from . import models

admin.site.register(models.Restaurant)
admin.site.register(models.Delivery)
admin.site.register(models.Driver)