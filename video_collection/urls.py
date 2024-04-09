"""
URLS FOR THE APP
each page needs a URL, View, and a Template
sometimes also will need a Form
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add', views.add, name='add_video')
]
