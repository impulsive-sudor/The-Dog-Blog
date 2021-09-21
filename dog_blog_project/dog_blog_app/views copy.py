from django.shortcuts import render, redirect




def new(request):
    # if 'user_id' not in request.session:
    #     return redirect('/ ')
    
    return render(request,'new.html')

def create(request):
    # if 'user_id' not in request.session:
    #     return redirect('/ ')
    
    errors = Apt.objects.update_validator(request.POST)
    if len(errors) > 0:
        for value in errors.values():
            messages.error(request, value)

        return redirect('/new')
    else:
        #createobject       
        logged_user = User.objects.get(id=request.session['user_id'])   

    #this is coming from the POST request in the form 
    Dog.objects.create(
        name=request.POST['name'],
        breed=request.POST['breed'],
        color=request.POST['color'],
        age=request.POST['age'],
        story=request.POST['story'],
        created_by = logged_user,
        owner = logged_user
        )
    return redirect('/')  