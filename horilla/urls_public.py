from django.contrib import admin
from django.urls import path
from django.http import HttpResponse

def index(request):
    from django.shortcuts import render
    return render(request, "landing_home.html")

from customers.views import saas_dashboard

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', saas_dashboard, name='saas_dashboard'),
    path('', index),
]
