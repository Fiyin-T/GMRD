from django.urls import path
from . import views

urlpatterns = [
    path('accounts/signup/',views.signup, name='signup'),
    path('', views.home, name='home'),
    path('games/genres/', views.game_genres, name='game_genres'),
    path('list/<int:list_id>/assoc_game/<int:game_id>/', views.assoc_game, name='assoc_game'),
    path('games/genre/<slug:genre>/', views.genre_index, name='genre_index'),
    path('games/<int:id>/', views.game_index, name='game_index'),
    path('lists/', views.lists_index, name='index'),
    path('lists/create/', views.ListCreate.as_view(), name='lists_create'),
    path('lists/<int:list_id>/', views.lists_detail, name='list_detail')
]