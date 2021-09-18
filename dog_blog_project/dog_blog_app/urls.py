from django.urls import path     
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index),
    path('uploadprofilepicture', views.uploadprofilepicture),
]

# This is setting is required to allow writing media files to local file system. Typically they are store on a CDN or in S3
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)