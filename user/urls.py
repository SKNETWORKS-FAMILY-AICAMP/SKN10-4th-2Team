from django.urls import path
from .views import user_logout, login_required

urlpatterns = [
    path('logout/', user_logout, name='user-logout'),
    path('login-register/', login_required, name='user-login-register')
]