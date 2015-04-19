from django.shortcuts import render
from forms import *
from django.forms.formsets import formset_factory
from delta3.models import Gif
from django.http import HttpResponse, HttpResponsePermanentRedirect

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
	if (request.REQUEST.get('searchterm')):
		g = Gif.objects.get(gif_name=request.REQUEST.get('searchterm'))
		if (g):
			# return HttpResponse(g.gif_url)
			return HttpResponsePermanentRedirect("/delta3/search")
		else:
			return HttpResponsePermanentRedirect("/delta3/search")
	return render(request, 'delta3/search.html', {'form': SearchForm})

def about(request):
	return render(request, 'delta3/about.html')

def register(request):
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