from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from . models import List, Game
import requests, os
from datetime import datetime
from bs4 import BeautifulSoup

# Create your views here.
def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('home')
    else:
      error_message = 'Invalid sign up - Try again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

def home(request):
  return render(request, 'home.html')

def game_genres(request):
  # games api stuff here
  url = 'https://api.rawg.io/api/genres?key={}'
  api_key = os.environ.get('API_KEY')
  game_data = requests.get(url.format(api_key)).json()
  genres = game_data['results']
  return render(request, 'games/genres.html', { 'genres': genres })
  
def assoc_game(request, list_id):
  title = request.POST['title']
  release_date = request.POST['release_date']
  description = request.POST['description']
  # print(Game.objects.filter(title))
  # List.objects.get(id=list_id).game.add(game_id)
  return redirect('game_genres')
  
def genre_index(request, genre):
  # games api stuff here
  url = 'https://api.rawg.io/api/games?key={}&genres={}'
  api_key = os.environ.get('API_KEY')
  game_data = requests.get(url.format(api_key, genre)).json()
  games = game_data['results']
  return render(request, 'games/genre_index.html', { 'games': games, 'genre': genre })

def game_index(request, id):
    url = 'https://api.rawg.io/api/games/{}?key={}'
    api_key = os.environ.get('API_KEY')
    game_data = requests.get(url.format(id, api_key)).json()
    strRelease = game_data['released']
    release = datetime.strptime(strRelease, '%Y-%m-%d').strftime('%b %d %Y')
    descriptionHtml = game_data['description']
    soup = BeautifulSoup(descriptionHtml, 'html5lib')
    description = soup.get_text()
    context = { 'game': game_data, 'release': release, 'description': description }
    return render(request, 'games/game_index.html', context)



  