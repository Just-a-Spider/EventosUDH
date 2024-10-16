from django.contrib import admin
from user import models

admin.site.register(models.Student)
admin.site.register(models.Coordinator)
admin.site.register(models.Speaker)
