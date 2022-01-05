from django.urls import path, re_path
from .views import *


urlpatterns = [
    path('', greet, name='greet'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('log/', LoginUser.as_view(), name='log'),
    path('main/', mainpage, name='main'),
]
