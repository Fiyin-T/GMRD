from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', views.signup, name='signup'),
    
    # view / create lists
    path('lists/', views.lists_index, name='index'),
    path('lists/create/', views.ListCreate.as_view(), name='lists_create'),
    path('lists/<int:list_id>/', views.lists_detail, name='list_detail'),
    
    # query through api to find game
    path('lists/<int:list_id>/games/genres/', views.game_genres, name='game_genres'),
    path('lists/<int:list_id>/games/genres/<slug:genre>/', views.genre_index, name='genre_index'),   
    path('lists/<int:list_id>/games/<int:game_id>/', views.game_index, name='game_index'),
    path('list/<int:list_id>/assoc_game/', views.assoc_game, name='assoc_game'),
    path('list/<int:list_id>/unassoc_game/<int:game_id>/', views.unassoc_game, name='unassoc_game'),
]