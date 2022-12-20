"""psm_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Renders
    path('', include('user_management.urls.render')),
    path('', include('internment_management.urls.render')),
    path('', include('financial.urls.render')),

    # APIs
    path('api/users/', include('user_management.urls.api')),
    path('api/internments/', include('internment_management.urls.internments')),
    path('api/referrals/', include('internment_management.urls.referrals')),
    path('api/invoices/', include('financial.urls.invoices')),
    path('api/stats/', include('financial.urls.stats')),
    path('api/datatables/', include('internment_management.urls.datatables')),
    path('api/financial/datatables/', include('financial.urls.datatables')),
]
