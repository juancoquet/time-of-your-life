"""timeofyourlife_v1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django import urls
from django.contrib import admin
from django.urls import include, path

from countdown import views as countdown_views
from .views import about

urlpatterns = [
    path('admin/', admin.site.urls),

    # djagno-allauth
    path('accounts/', include('allauth.urls')),
    # Custom signup view
    path('accounts/', include('accounts.urls')),

    # Local apps
    path('grid/', include('countdown.urls')),
    path('', countdown_views.home, name='home'),
    path('contact/', include('contact.urls')),
    path('about/', about, name='about'),
]
