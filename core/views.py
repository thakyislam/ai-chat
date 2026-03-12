from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render,redirect
from django.conf import settings
# Create your views here.


openai_key = settings.OPENAI_API_KEY

@login_required
def home(request):
    return render(request, 'core/home.html')

@require_GET
def logout_view(request):
    logout(request)
    return redirect('login')

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})