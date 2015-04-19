from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
	url(r'^delta3/', include('delta3.urls')),
	url(r'^admin/', include(admin.site.urls)),
	#url(r'^secure_app/', include('secure_app.urls')),
)

urlpatterns += staticfiles_urlpatterns()
