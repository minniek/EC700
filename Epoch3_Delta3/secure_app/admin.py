from django.contrib import admin

from .models import Request, Filter

class RequestAdmin(admin.ModelAdmin):
	list_display = ('timestamp', 'full_url', 'is_good', 'param_map')
	list_filter = ['is_good', 'full_url']

admin.site.register(Request, RequestAdmin)

class FilterAdmin(admin.ModelAdmin):
	list_display = ('url_path', 'field_name', 'regex_filter')

admin.site.register(Filter, FilterAdmin)
