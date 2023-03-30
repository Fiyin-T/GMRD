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
    path('lists/<int:pk>/delete', views.ListDelete.as_view(), name='list_delete'),
    path('list/<int:pk>/edit', views.ListUpdate.as_view(), name='list_edit'),
    
    # query through api to find game
    path('lists/<int:list_id>/games/genres/', views.game_genres, name='game_genres'),
    path('lists/<int:list_id>/games/genres/<slug:genre>/', views.genre_index, name='genre_index'),   
    path('lists/<int:list_id>/games/<int:game_id>/', views.game_index, name='game_index'),
    path('list/<int:list_id>/assoc_game/', views.assoc_game, name='assoc_game'),
    path('list/<int:list_id>/unassoc_game/<int:game_id>/', views.unassoc_game, name='unassoc_game'),
    
    # Game URLs
    path('games/<int:game_id>/', views.game_detail, name='game_detail'),
    path('lists/<int:list_id>/games/search/', views.search, name='search'),
]