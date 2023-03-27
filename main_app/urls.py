from django.urls import path
from . import views

urlpatterns = [
    path('accounts/signup/',views.signup, name='signup'),
    path('', views.home, name='home'),
    path('games/genres/', views.game_genres, name='game_genres'),
    # path('games/genre/', views.game_search, name=''),
    # path('games/search/', views.game_search, name='search'),
]