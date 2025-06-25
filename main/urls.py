from django.contrib import admin
from django.urls import path, include 

from . import views 
from .views import contact_view



urlpatterns = [
    path('', views.Index, name = 'index'),
	path('contact/', contact_view, name='contact'),
]
