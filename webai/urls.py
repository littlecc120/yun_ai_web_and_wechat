
from django.contrib import admin
from django.urls import path, include
from webai.views import chat_view

urlpatterns = [
    path('webai/', chat_view, name='webai')
]
