
from django.urls import path
from . import views

urlpatterns = [
    path('', views.user, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('contact/', views.contact, name='contact'),  
]
