from django.shortcuts import render, redirect


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
        return redirect('/')
    else:
        context = {
            'users': User.objects.get(id=request.session['user_id'])
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