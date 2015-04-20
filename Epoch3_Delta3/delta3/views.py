from django.shortcuts import render
from forms import *
from django.forms.formsets import formset_factory
from delta3.models import Gif
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.db import connection

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
	if request.method == 'POST':
		if(request.REQUEST.get('searchterm')):
			searchterm = str(request.REQUEST.get('searchterm'))
			sql = 'SELECT * from delta3_gif where gif_name=' + '"' + searchterm + '"' 
			g = Gif.objects.raw(sql)
			# g = Gif.objects.raw('SELECT * from delta3_gif where gif_name=""; SELECT * from delta3_user')
			if (g):
				response = ""
				for x in g:	
					response = response + str(x) + "<br>"
					url = str(x.gif_url)
				html = "<img src=" + url + "\>"
				return HttpResponse(html)
	return render(request, 'delta3/search.html', {'form': SearchForm})

def about(request):
	return render(request, 'delta3/about.html')

def register(request):
	# Exceptions are manually being created for POC
	# These exceptions will handled by the middlewares.py's "process_exception"
	# Raise ValueError exception if a digit is in firstname or lastname
	if (request.REQUEST.get('firstname')):
		firstname_in = request.REQUEST.get('firstname')
		if any(char.isdigit() for char in firstname_in):
			raise ValueError("Integer detected in firstname in /delta3/register")

	if (request.REQUEST.get('lastname')):
		lastname_in = request.REQUEST.get('lastname')
		if any(char.isdigit() for char in lastname_in):
			raise ValueError("Integer detected in lastname in /delta3/register")

	# Raise ValueError exception if a character is found in the grad_year
	if(request.REQUEST.get('grad_year')):
		x = int(request.REQUEST.get('grad_year'))
		# try: 
		# 	x = int(request.POST.get('grad_year'))
		# except ValueError:
		# 	return HttpResponse("ValueError exception thrown")
	return render(request, 'delta3/register.html', {'form': RegisterForm})

def thanks(request):
	return render(request, 'delta3/thanks.html')

def secure_app(request):
	return render(request, 'delta3/secure_app.html')