from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from hospitalauth.models import HospitalUser


admin.site.register(HospitalUser)

# Register your models here.
