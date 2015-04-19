from django.shortcuts import render
from forms import *
from django.forms.formsets import formset_factory

def home(request):
	return render(request, 'delta3/home.html')

def strings(request):
	return render(request, 'delta3/strings.html', {'form': StringsForm})

def numbers(request):
	return render(request, 'delta3/numbers.html', {'form': NumbersForm})
	
def login(request):
	return render(request, 'delta3/login.html', {'form': LoginForm})

def comments(request):
	return render(request, 'delta3/comments.html', {'form': CommentsForm})

def search(request):
	return render(request, 'delta3/search.html', {'form': SearchForm})

def about(request):
	return render(request, 'delta3/about.html')

def register(request):
	return render(request, 'delta3/register.html', {'form': RegisterForm})

def thanks(request):
	return render(request, 'delta3/thanks.html')

def secure_app(request):
	return render(request, 'delta3/secure_app.html')