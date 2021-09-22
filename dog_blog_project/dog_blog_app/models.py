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
            errors['email_used'] = "This emaill address has registered by someone else."

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


GENDER_CHOICES =(
    ("male", "male"), 
    ("female", "female"), 
    ("other", "other")
)

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



class DogManager(models.Manager):
    def update_validator(self, postData):
        errors ={}

        if len(postData['name']) < 2:
            errors['name'] = "Dog's name can not be that short"
        if len(postData['breed']) < 1:
            errors['breed'] = "Breed cannot be blank."    
        if len(postData['color']) < 1:
            errors['color'] = "Color cannot be blank."     
        if len(postData['age']) < 1:
            errors['age'] = "Age cannot be blank." 
    
        if len(postData['story']) < 3:
            errors['story'] = "Story cannot be blank."      
        
        return errors




class Dog(models.Model):
    name = models.CharField(max_length=20)
    breed = models.CharField(max_length=20)
    color = models.CharField(max_length=20)
    age = models.CharField(max_length=20)
    story = models.CharField(max_length=250)
    created_at =  models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, related_name="dogs_created", on_delete = models.CASCADE)
    owner = models.ForeignKey(User, related_name="dogs_owned", on_delete = models.CASCADE)

    objects = DogManager()