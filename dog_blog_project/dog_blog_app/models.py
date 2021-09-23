from django.db import models
import re
from django.utils import timezone

class UserManager(models.Manager):
    def register_validation(self,post_data):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        FIRST_NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
        LAST_NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

        #validate first name
        if post_data['first_name'] == '':
            errors['first_name_empty'] = "First name is required!!"
        elif len(post_data['first_name']) < 2 :
            errors['first_name_length'] = "First name has at least 2 characters."
        elif not FIRST_NAME_REGEX.match(post_data['first_name']):
            errors['first_name'] = "First name must be letters!"

        #validate last name
        if post_data['last_name'] == '':
            errors['last_name_empty'] = "Last name is required!!"
        elif len(post_data['last_name'])< 2:
            errors['last_name_length'] = "Last name has at least 2 characters."
        elif not LAST_NAME_REGEX.match(post_data['last_name']):
            errors['last_name'] = "Last name must be letters!"

        #validate email
        users = User.objects.filter(email = post_data['email'])
        if post_data['email'] == '':
            errors['email_empty'] = "Email is required!!"
        elif not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Invalid email address!"
        elif users:
            errors['email_used'] = "This emaill address has been registered by someone else."

        #validate password
        if post_data['password'] == '':
            errors['password_empty'] = "Password is required!!"
        elif len(post_data['password']) < 8:
            errors['password_length'] = "Password has at least 8 characters."

        if post_data['password'] != post_data['confirm_password']:
            errors['password_not_match'] = "Password Not Match!!!"

        #validate birthdate
        if post_data['birthdate'] == '':
            errors['birthdate_empty'] = "Please select a birthdate"

        return errors

    def login_validation(self,post_data):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

        #validate login email address
        if post_data['email'] == '':
            errors['email_empty'] = "Please enter your Login Email!!"
        elif not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Invalid email address!"

        # password can not be empty
        elif post_data['password'] == '':
            errors['password_empty'] = "Password is required!"

        return errors

    def edit_validation(self, post_data):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        FIRST_NAME_REGEX = re.compile(r'^[a-zA-Z]+$')
        LAST_NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

        #validate first name
        if post_data['first_name'] == '':
            errors['first_name_empty'] = "First name is required!!"
        elif len(post_data['first_name']) < 2 :
            errors['first_name_length'] = "First name has at least 2 characters."
        elif not FIRST_NAME_REGEX.match(post_data['first_name']):
            errors['first_name'] = "First name must be letters!"

        #validate last name
        if post_data['last_name'] == '':
            errors['last_name_empty'] = "Last name is required!!"
        elif len(post_data['last_name'])< 2:
            errors['last_name_length'] = "Last name has at least 2 characters."
        elif not LAST_NAME_REGEX.match(post_data['last_name']):
            errors['last_name'] = "Last name must be letters!"

        #validate email
        if post_data['email'] == '':
            errors['email_empty'] = "Email is required!!"
        elif not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = "Invalid email address!"

        #validate birthdate
        if post_data['birthdate'] == '':
            errors['birthdate_empty'] = "Please select a birthdate"

        #validate country
        if post_data['country'] == '':
            errors['country_empty'] = "Please enter your country"

        #validate address
        if post_data['address'] == '':
            errors['address_empty'] = "Please enter your address"

        #validate phone
        if post_data['phone'] == '':
            errors['phone_empty'] = "Please enter your phone number"

        return errors

class DogimageManager(models.Manager):
    def dog_validation(self, post_data):
        errors = {}

        # dog name validation
        if post_data['dog_name'] == '':
            errors['dog_name_empty'] = "Please fill in your dog name"
        elif len(post_data['dog_name']) < 2:
            errors['dog_name_length'] = "Dog name needs at least 2 characters"

        # dog's breed validation
        if post_data['breed'] =='':
            errors['breed_empty'] = "Please tell us your dog's breed"
            
        # dog's color validation
        if post_data['color'] == '':
            errors['color_empty'] = "Dog's color must be filled"

        # dog's age validation
        if post_data['age'] == '':
            errors['age_empty'] = "Dog's age can not be empty"
        elif int(post_data['age']) < 0:
            errors['age_negative'] = "The dog's age can not be negative"

        # dog's desc validation
        if post_data['desc'] == '':
            errors['desc_empty'] = "Please tell us something interesting about your dog!"
        elif len(post_data['desc']) < 4 :
            errors['desc_length'] = "Description has at least 4 characters"

        return errors


GENDER_CHOICES =(
    ("male", "male"), 
    ("female", "female"), 
    ("other", "other")
)

class CommentManager(models.Manager):
    def comment_validation(self, post_data):
        errors = {}
        # comment post validation
        if post_data['statement'] == '':
            errors['statement_empty'] = "Comments can't be empty"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    birthdate = models.DateTimeField(default=timezone.now)
    profitimage = models.ImageField(upload_to='profitimages/', blank= True, null=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=255)

    country = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Post(models.Model):
    dog_name = models.CharField(max_length=255)
    color = models.CharField(max_length=255)
    breed = models.CharField(max_length=255)
    age = models.IntegerField(default=0)
    desc = models.CharField(max_length=255)
    dogimage = models.ImageField(upload_to='dogimages/', blank= True, null=True, default="none")
    posted_by = models.ForeignKey(User, related_name="user_post", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = DogimageManager()
    favorites = models.ManyToManyField(User, related_name="favorited_posts")

class Comment(models.Model):
    statement = models.CharField(max_length=500)
    owner = models.ForeignKey(User, related_name='user_comments', on_delete=models.CASCADE)
    commented_on = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = CommentManager()


class Friend(models.Model):
    #users is the friends list, this_user is whoever's logged in's friends list
    #to many with this_user, many to many with users
    users = models.ManyToManyField(User, related_name='friend_set')
    this_user = models.ForeignKey(User, related_name='owner', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
