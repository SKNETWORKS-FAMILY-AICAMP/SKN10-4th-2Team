from django.shortcuts import render

def index(request):
    # http://www.localhost:8000/user/index/
    return render(request, 'user/index.html')

def login_register(request):
    # http://www.localhost:8000/user/login_register/
    return render(request, 'user/login_register.html')