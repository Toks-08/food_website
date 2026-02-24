from django.contrib import admin
from .models import CustomUser, Referral,EmailOTP

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Referral)
admin.site.register(EmailOTP)