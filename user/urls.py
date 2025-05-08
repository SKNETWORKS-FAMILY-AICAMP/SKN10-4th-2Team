from django.urls import path
from .views import index, login_register

# http://www.localhost:8000/user/*
urlpatterns = [
    path('index/', index, name='user-index'),  # http://www.localhost:8000/user/index/
    path('login_register/', login_register, name='user-login_register'),  # http://www.localhost:8000/user/login_register/
]
