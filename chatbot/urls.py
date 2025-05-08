from django.contrib import admin
from django.urls import path
from .views import index, chat

# http://www.localhost:8000/*
urlpatterns = [
    path('', index, name='chatbot-index'),  # http://www.localhost:8000/
    path('chat/', chat, name='chatbot-chat'),  # http://www.localhost:8000/chat/
]
