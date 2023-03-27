from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

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
  api_key = os.environ.get('API_KEY=4c23650312994d429b5e93b4f7b8b1f5')
  game_data = requests.get(url.format(api_key)).json()
  genres = game_data['results']
  return render(request, 'games.html', { 'genres': genres, 'game_data':game_data})
  
