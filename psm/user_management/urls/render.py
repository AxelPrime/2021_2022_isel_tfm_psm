from django.urls import path

from ..views.render import *


urlpatterns = [
    path('login/', login_page),
]
