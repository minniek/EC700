from django.db import models

class User(models.Model):
	username = models.CharField(max_length=35)
	password = models.CharField(max_length=200)

	def __unicode__(self):
		return "username :" + str(self.username) + ", password : " + str(self.password)

class Gif(models.Model):
	gif_name = models.CharField(max_length=20)
	gif_url = models.URLField(max_length=200)

	def __unicode__(self):
		return "gif_name :" + str(self.gif_name) + ", gif_url : " + str(self.gif_url)

