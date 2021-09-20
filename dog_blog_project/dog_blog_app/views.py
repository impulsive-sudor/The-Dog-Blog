from django.shortcuts import render, redirect
import bcrypt
from django.contrib import messages
from .models import User

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
        return redirect('/edit_page')
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
                return redirect('/edit_page')
            else:
                messages.error(request, "Email or Password not match!", extra_tags='login')

        if not user:
            messages.error(request,"This email address not register yet!!! Please go to register!", extra_tags='login')

    return redirect('/login_register')

def edit_page(request):
    if "user_id" not in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id = request.session['user_id'])
        context = {
            'user': user
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
        context = {
            'users': User.objects.get(id=request.session['user_id']),
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