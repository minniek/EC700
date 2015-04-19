from django.db import models

class LoginInfo(models.Model):
	username = models.CharField(max_length=35)
	password = models.CharField(max_length=200)

class Search(models.Model):
	gif_name = models.CharField(max_length=20)
	gif_url = models.URLField(max_length=200)