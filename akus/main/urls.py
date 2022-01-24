from django.urls import path, re_path
from .views import *
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', greet, name='greet'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('log/', LoginUser.as_view(), name='log'),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('main/', mainpage, name='main'),
    path('skills/manage/', manage_skills, name='manage_skills'),
    path('bands/list/', manage_bands, name='manage_bands'),
    path('bands/add/', create_new_band, name='create_new_band'),
    path('bands/update/', update_band, name='update_band'),
    path('bands/update/<int:vacation_id>/', update_band_get, name='update_band_get'),
]
