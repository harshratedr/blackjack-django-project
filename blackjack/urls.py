from django.urls import path
from . import views

urlpatterns = [
    path('game/', views.game, name='game'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    path('user_stats/', views.user_stats, name='user_stats'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
]