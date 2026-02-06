from django.urls import path
from .views import (
    add_donor,
    donor_list,
    edit_donor,
    delete_donor,
    search_donors,
    kiosk_view,
)

urlpatterns = [
    path('add/', add_donor, name='add_donor'),
    path('list/', donor_list, name='donor_list'),
    path('edit/<int:id>/', edit_donor, name='edit_donor'),
    path('delete/<int:id>/', delete_donor, name='delete_donor'),
    path('search/', search_donors, name='search_donors'),
    path('kiosk/',kiosk_view,name='kiosk'),
]
