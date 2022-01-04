from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from mailservice import views
urlpatterns = [
    path("",views.index,name="home")
]