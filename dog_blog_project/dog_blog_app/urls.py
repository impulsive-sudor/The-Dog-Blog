from dog_blog_app.models import Comment
from django.urls import path     
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home),

    #Nick works here
    path('login_register', views.login_register),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('edit_page', views.edit_page),
    path('user_edit', views.user_edit),

    path('submission_page', views.submission_page),
    path('create_post', views.create_post),

    path('favorite_post/<int:Post_id>', views.favorite_post),
    path('unfavorite_post/<int:Post_id>', views.unfavorite_post),
    #Christian's adds
    #GET
    path('<int:User_id>/friends',views.friends_list),
    path('post/<int:post_id>',views.view_post),
    #POST
    path('comment/<int:post_id>',views.post_comment),
    path('add_friend/<int:User_id>',views.add_friend),
    path('lose_friend/<int:User_id>',views.lose_friend)
]

# This is setting is required to allow writing media files to local file system. Typically they are store on a CDN or in S3
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)