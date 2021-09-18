from django.shortcuts import render, redirect

# This code is to upload a profile picture, need to intergrate into user creation form
def uploadprofilepicture(request):
    if request.method == 'POST':
        form = uploadprofilepicture(request.POST, request.FILES)
        if form.is_valid():
            instance = User(filepath=request.FILES['file'],title=request.POST['title'])
            instance.save()
            return redirect('/home')
    else:
        form = uploadprofilepicture()
    return render(request, 'profilepictureform.html', {'form': form})

