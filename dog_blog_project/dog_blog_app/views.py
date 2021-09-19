
from django.db.models.expressions import Exists
from django.shortcuts import render, redirect, HttpResponse
from .models import *

# Nick is working on this
def register(request):
    return render(request, 'register.html')

# Nick is working on this
def login(request):
    return render(request, 'login.html')

def logout(request):
    request.session.flush()

    return redirect('/')

def user_edit(request):
    if "user_id" not in request.session:
        return HttpResponse('/')
    else:
        context = {
            'user': User.objects.get(id=request.session['user_id'])
        }
        return render(request, "edit_user.html", context)

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
        user = User.objects.get(id=request.session["user_id"])
        friends_posts = Post.objects.filter(this_user=user)
        non_friends_posts = Post.objects.exclude(this_user=user)
        context = {
            'user': user,
            'posts': Post.objects.all(),
            'friends_posts' : friends_posts,
            'non_friends_posts' : non_friends_posts
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
def friends_list(request):
    if "user_id" not in request.session:
        return HttpResponse("Only Registered Users can access a Friends List!")
    else:
        user = User.objects.get(id=request.session["user_id"])
        friends = Friend.objects.get(this_user=user)
        context= {
            'user' : user,
            'friends' : friends
        }
        return (request, 'friends_list.html', context)

def view_post(request, Post_id):
    if "user_id" not in request.session:
        return HttpResponse("Only Registered Users can view Blog pages!")
    else:
        post = Post.objects.get(id=Post_id)
        comments = Comment.objects.filter(commented_on=post)
        user = User.objects.get(id=request.session["user_id"])
        #counter of how many people favorited post
        favorites = post.favorites.all()
        count_favorites = {}
        count_favorites = favorites.values()
        context= {
            'post' : post,
            'comments' : comments,
            'user' : user,
            'count' : len(count_favorites)
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