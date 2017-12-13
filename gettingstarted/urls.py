from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

from django.conf.urls.static import static
from django.conf import settings

import hello.views


urlpatterns = [
    # youtube 视频下载
    url(r'^youtube/', include('youtube.urls', namespace='youtube')),

    # hello 支付宝和微信二维码合并
    url(r'^', include('hello.urls', namespace='hello')),

    # 站点 mysite
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
