from django.contrib import admin
from mail import models

# Register your models here.
admin.site.register(models.Email)
admin.site.register(models.User)