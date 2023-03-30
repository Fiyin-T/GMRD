from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from . models import List, Game
import requests, os
from datetime import datetime
from bs4 import BeautifulSoup
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.models import User

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
  lists = List.objects.all()
  return render(request, 'home.html', { 'lists': lists })

def game_genres(request, list_id):
  # games api stuff here
  url = 'https://api.rawg.io/api/genres?key={}'
  api_key = os.environ.get('API_KEY')
  game_data = requests.get(url.format(api_key)).json()
  genres = game_data['results']
  return render(request, 'games/genres.html', { 'genres': genres, 'list_id': list_id })

def genre_index(request, list_id, genre):
  # games api stuff here
  url = 'https://api.rawg.io/api/games?key={}&genres={}'
  api_key = os.environ.get('API_KEY')
  game_data = requests.get(url.format(api_key, genre)).json()
  games = game_data['results']
  return render(request, 'games/genre_index.html', { 'games': games, 'genre': genre, 'list_id': list_id })

def game_index(request, list_id, game_id):
    url = 'https://api.rawg.io/api/games/{}?key={}'
    api_key = os.environ.get('API_KEY')
    game_data = requests.get(url.format(game_id, api_key)).json()
    strRelease = game_data['released']
    release = datetime.strptime(strRelease, '%Y-%m-%d').strftime('%b %d %Y')
    descriptionHtml = game_data['description']
    screenshot = game_data['background_image']
    soup = BeautifulSoup(descriptionHtml, 'html5lib')
    description = soup.get_text()
    context = { 'game': game_data, 'release': release, 'description': description, 'list_id': list_id, 'screenshot': screenshot}
    return render(request, 'games/game_index.html', context)

@login_required
def assoc_game(request, list_id):
  title = request.POST['title']
  list = List.objects.get(id=list_id)
  if (Game.objects.filter(title=title)):
    # grab the instance of the game that exists in the database
    game = Game.objects.get(title=title)
  else:
    # add the game to the database and grab the new item
    game = Game.objects.create(
      title = request.POST['title'],
      release_date = datetime.strptime(request.POST['release_date'], '%b %d %Y'),
      description = request.POST['description'],
      screenshot_url = request.POST['screenshot']
    )
  # associate the game to the list
  list.game.add(game.id)
  return redirect('list_detail', list_id=list_id )

@login_required
def unassoc_game(request, list_id, game_id):
  List.objects.get(id=list_id).game.remove(game_id)
  return redirect('list_detail', list_id=list_id )

class ListCreate(LoginRequiredMixin, CreateView):
  model = List
  fields = ['name', 'date_created']
  success_url = '/lists/'

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

@login_required
def lists_index(request):
  lists = List.objects.filter(user = request.user)
  return render(request, 'lists/index.html', { 'lists': lists })

@login_required
def lists_detail(request, list_id):
  list = List.objects.get(id=list_id)
  return render(request, 'lists/list_detail.html', { 'list': list })

class ListDelete(LoginRequiredMixin, DeleteView):
  model = List
  success_url = '/lists/'

class ListUpdate(LoginRequiredMixin, UpdateView):
  model = List
  fields = ['name']

def search(request, list_id):
  # games api search
  url = 'https://api.rawg.io/api/games?key={}&search={}'
  search_raw = request.POST['search']
  search = search_raw.replace(' ', '-')
  api_key = os.environ.get('API_KEY')
  game_data = requests.get(url.format(api_key, search)).json()
  games = game_data['results']
  return render(request, 'games/search.html', { 'search': search_raw, 'games': games, 'list_id': list_id } )