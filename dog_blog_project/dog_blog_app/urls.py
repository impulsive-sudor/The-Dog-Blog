from django.urls import path     
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home),
    path('uploadprofilepicture', views.uploadprofilepicture),

    #Nick works here
    path('login_register', views.login_register),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('edit_page', views.edit_page),
    path('user_edit', views.user_edit),

    path('submission_page', views.submission_page),
    path('favorite_post/<int:post_id>', views.favorite_post),
    path('favorite_post/<int:post_id>', views.unfavorite_post)
]

# This is setting is required to allow writing media files to local file system. Typically they are store on a CDN or in S3
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)