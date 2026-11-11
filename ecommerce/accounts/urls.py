
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.User_register, name='register'),
    path('signin/', views.User_login, name='signin'),
    path('logout/', views.User_logout, name='logout'),
    path('profile/', views.User_profile, name='profile'),

]
