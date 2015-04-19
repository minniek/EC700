from django import forms

class StringsForm(forms.Form):
	firstname = forms.CharField(max_length=35)
	lastname = forms.CharField(max_length=35)

class NumbersForm(forms.Form):
	num1 = forms.IntegerField()
	num2 = forms.IntegerField()

class LoginForm(forms.Form):
	username = forms.CharField(max_length=35)
	password = forms.CharField(widget=forms.PasswordInput()) # Set min_length later...

class CommentsForm(forms.Form):
	comments = forms.CharField(widget=forms.Textarea)

class SearchForm(forms.Form):
	searchterm = forms.CharField(max_length=35)
	results = forms.CharField(max_length=35)

class RegisterForm(forms.Form):
	firstname = forms.CharField(max_length=35)
	lastname = forms.CharField(max_length=35)
	grad_year = forms.CharField(max_length=4)
