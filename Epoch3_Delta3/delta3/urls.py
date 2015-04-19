from django.conf.urls import url
from . import views

# Add views for app "polls" here
urlpatterns = [
	# /delta3
    url(r'^$', views.home, name='home'),
    # /delta3/strings
	url(r'^strings', views.strings, name='strings'),
	# /delta3/numbers
	url(r'^numbers', views.numbers, name='numbers'),
	# /delta3/login
	url(r'^login', views.login, name='login'),
	# /delta3/register
	url(r'^register', views.register, name='register'),
	# /delta3/comments
	url(r'^comments', views.comments, name='comments'),
	# /delta3/search
	url(r'^search', views.search, name='search'),
	# /delta3/about
	url(r'^about', views.about, name='about'),
	# /delta3/thanks
	url(r'^thanks', views.thanks, name='thanks'),
	# /delta3/secure_app
	url(r'^secure_app', views.secure_app, name='secure_app'),
]