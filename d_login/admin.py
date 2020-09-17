from django.contrib import admin
from . import models
# Register your models here.

admin.site.register(models.UserData)
admin.site.register(models.UserDataHistory)
admin.site.register(models.UserProjectData)

