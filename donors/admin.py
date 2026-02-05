from django.contrib import admin
from .models import Donor
# Register your models here.
@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display=('name','blood_group','gender','age','mobile','area')
    search_fields=('name','mobile','area')
    list_filter=('blood_group','gender')
    