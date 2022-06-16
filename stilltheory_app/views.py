from django.shortcuts import render

def index(request):
    return username_testpage(request)

def username_testpage(request):
    return render(request, 'stilltheory_app/username.html', {})