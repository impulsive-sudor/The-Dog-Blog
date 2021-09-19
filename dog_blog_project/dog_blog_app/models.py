from django.db import models

# made dummy classes for User and Post
class User(models.Model):
    first_name= models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Post(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Comment(models.Model):
    statement = models.CharField(max_length=500)
    owner = models.ForeignKey(User, related_name='user_comments', on_delete=models.CASCADE)
    commented_on = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Friend(models.Model):
    #users is the friends list, this_user is who's logged in's friends list
    #to many with this_user, many to many with users
    users = models.ManyToManyField(User, related_name='friend_set')
    this_user = models.ForeignKey(User, related_name='owner', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)