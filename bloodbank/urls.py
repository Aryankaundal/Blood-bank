from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.views import LogoutView

from donors.views import home, login_view, signup_view


def staff_only(user):
    return user.is_staff


urlpatterns = [
    path('admin/',admin.site.urls),

    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('signup/', signup_view, name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('donors/', include('donors.urls')),
]
