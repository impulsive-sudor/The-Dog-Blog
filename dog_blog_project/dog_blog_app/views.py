from django.shortcuts import render, HttpResponse

# just for testing, we can delete these lines later
def index(request):
    return HttpResponse("This is my response!")
