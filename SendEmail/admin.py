from django.contrib import admin

from . import models
# Register your models here.
admin.site.register(models.SuperAdmin)
admin.site.register(models.Users)
admin.site.register(models.EmailData)
admin.site.register(models.EmailLog)
admin.site.register(models.ReceivedEMail)