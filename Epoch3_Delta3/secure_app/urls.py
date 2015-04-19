from django.conf.urls import url
from . import views

# Add views for app "polls" here
urlpatterns = [
	# /delta3/evil
    url(r'^evil$', views.evil, name='evil'),
]