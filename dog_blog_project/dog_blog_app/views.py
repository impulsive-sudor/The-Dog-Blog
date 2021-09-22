from django.db.models.expressions import Exists
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import *
import bcrypt

# Nick is working on this
def login_register(request):
    return render(request, "register_login.html")

def register(request):
    errors = User.objects.register_validation(request.POST)
    if errors:
        for value in errors.values():
            messages.error(request, value, extra_tags="register")

    else:
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt()).decode()

        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = pw_hash,
            birthdate = request.POST['birthdate']
        )
        request.session['user_id'] = user.id
        return redirect('/')
    return redirect('/login_register')

# Nick is working on this
def login(request):
    errors = User.objects.login_validation(request.POST)
    if errors: 
        for value in errors.values():
            messages.error(request, value, extra_tags='login')

    else:
        user = User.objects.filter(email = request.POST['email'])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                return redirect('/')
            else:
                messages.error(request, "Email or Password not match!", extra_tags='login')

        if not user:
            messages.error(request,"This email address not register yet!!! Please go to register!", extra_tags='login')

    return redirect('/login_register')

def edit_page(request):
    if "user_id" not in request.session:
        return HttpResponse('/')
    else:
        user = User.objects.get(id = request.session['user_id'])
        context = {
            'user': User.objects.get(id=request.session['user_id'])
        }
        return render(request, "edit_page.html", context)

def user_edit(request):
    errors = User.objects.edit_validation(request.POST)
    if errors:
        for value in errors.values():
            messages.error(request, value)
    else:
        update_user = User.objects.get(id=request.session['user_id'])
        update_user.first_name = request.POST['first_name']
        update_user.last_name = request.POST['last_name']
        update_user.email = request.POST['email']
        update_user.birthdate = request.POST['birthdate']
        update_user.country = request.POST['country']
        update_user.address = request.POST['address']
        update_user.profitimage = request.FILES['profitimage']
        update_user.phone = request.POST['phone']
        if 'gender' not in request.POST:
            messages.error(request, "Please select your gender")
            return redirect('/edit_page')
        else: 
            update_user.gender = request.POST['gender']
        update_user.save()
        return redirect('/user_page')
    return redirect('/edit_page')

def user_page(request):
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user' : user
    }
    return render(request,'user_page.html', context)

def logout(request):
    request.session.flush()
    return redirect('/login_register')

# VanAnn is creating this
def submission_page(request):
    if "user_id" not in request.session:
        return redirect('/register')
    return render(request, 'submission_page.html')

def home(request):
    if "user_id" not in request.session:
        context = {
            'posts': Post.objects.all()
        }
        return render(request, "home.html", context)
    else:
        #added friends list/non friends list filter to sort posts
        #friends list was breaking the page so I commented it out for now
        user = User.objects.get(id=request.session["user_id"])
        #friends_posts = Post.objects.filter(this_user=user)
        #non_friends_posts = Post.objects.exclude(this_user=user)
        context = {
            'user': user,
            'posts': Post.objects.all()
        }
        
        return render(request, "home.html", context)
    

# This code is to upload a profile picture, need to intergrate into user creation form
def uploadprofilepicture(request):
    if request.method == 'POST':
        form = uploadprofilepicture(request.POST, request.FILES)
        if form.is_valid():
            instance = User(filepath=request.FILES['file'],title=request.POST['title'])
            instance.save()
            return redirect('/')
    else:
        form = uploadprofilepicture()
    return render(request, 'profilepictureform.html', {'form': form})

def favorite_post(request, post_id):
    post = Post.objects.get(id=post_id)
    user = User.objects.get(id=request.session["user_id"])
    user.favorited_by.add(post)

    return redirect('/')

def unfavorite_post(request, post_id):
    post = Post.objects.get(id=post_id)
    user = User.objects.get(id=request.session["user_id"])
    user.favorited_by.remove(post)

    return redirect('/')
    
#Christian's adds ---------------------------


#GET-----------------------------------------
def friends_list(request, User_id):
    if "user_id" not in request.session:
        return HttpResponse("Only Registered Users can access a Friends List!")
    else:
        if User_id in Friend.objects.filter(this_user=User_id):
            user = User.objects.get(id=request.session["user_id"])
            friends = Friend.objects.get(this_user=user)
            context= {
                'user' : user,
                'friends' : friends
            }
            return (request, 'friends_list.html', context)
        else:
            return HttpResponse("Get some friends!")

def view_post(request, Post_id):
    if "user_id" not in request.session:
        return HttpResponse("Only Registered Users can view Blog pages!")
    else:
        post = Post.objects.get(id=Post_id)
        comments = Comment.objects.filter(commented_on=post)
        user = User.objects.get(id=request.session["user_id"])
        all_users = User.objects.all()
        #counter of how many people favorited post
        favorites = post.favorites.all()
        count_favorites = {}
        count_favorites = favorites.values()
        context= {
            'post' : post,
            'comments' : comments,
            'user' : user,
            'count' : len(count_favorites),
            'all_users' : all_users
        }
        return (request,'view_post.html', context)


#POST----------------------------------------
def post_comment(request, Post_id):
    if request.method == "GET":
        return redirect('/')
    if "user_id" not in request.session:
        return HttpResponse("Only Registered Users can Post a Comment!")
    else:
        post = Post.objects.get(id=Post_id)
        user = User.objects.get(id=request.session["user_id"])
        Comment.objects.create(
            statement = request.POST['statement'],
            owner = user,
            commented_on = post
        )
        return (f"/post/{Post_id}")

def add_friend(request, User_id):
    if request.method == "GET":
        return redirect('/')
    if "user_id" not in request.session:
        return HttpResponse("Only Registered Users can add Friends!")
    else:
        user_friend = User.objects.get(id=User_id)
        user = User.objects.get(id=request.session["user_id"])
        if Friend.objects.get(this_user = user).exists() :
            add_friend = Friend.objects.get(this_user = user)
            user_friend = User.objects.get(id=User_id)
            add_friend.users.add(user_friend)
        else:
            Friend.objects.create(
            users = user_friend,
            this_user = user
            )
        return redirect('/home')

def lose_friend(request, User_id):
    if request.method == "GET":
        return redirect('/')
    if "user_id" not in request.session:
        return redirect("Only Registered Users can remove Friends!")
    else:
        user = User.objects.get(id=User_id)
        remove_friend = Friend.objects.get(this_user = user)
        user_friend = User.objects.get(id=User_id)
        remove_friend.users.remove(user_friend)
        return redirect('/home')