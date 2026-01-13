from django.contrib import admin
from django.urls import path
from django.http import HttpResponse

def index(request):
    from django.shortcuts import render
    return render(request, "landing_home.html")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
]
