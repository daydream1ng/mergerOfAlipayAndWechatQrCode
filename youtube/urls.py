from django.conf.urls import include, url
from . import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^search/$', views.search, name='search'),
    url(r'^video/$', views.video, name='video'),
    url(r'^verifyReceipt/$', views.verifyReceipt, name='verifyReceipt'),
]
