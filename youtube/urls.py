from django.conf.urls import include, url
from . import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^search$', views.search, name='search'),
]
