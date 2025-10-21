from django.urls import path
from . import views

# URLCONFIG

urlpatterns = [
    path('hello/', views.say_hello)
]