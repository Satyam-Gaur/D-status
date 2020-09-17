from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserData

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','password2','password1','username']

    username = forms.IntegerField(required=True,widget=forms.TextInput(attrs={'class': "form-control ",'type':'number'}))
    first_name = forms.CharField(required=True,widget=forms.TextInput(attrs={'class': "form-control",'type':'text'}))
    last_name = forms.CharField(required=True,widget=forms.TextInput(attrs={'class': "form-control",'type':'text'}))
    password1 = forms.CharField(required=True,widget=forms.TextInput(attrs={'class': "form-control",'type':'password'}))
    password2 = forms.CharField(required=True,widget=forms.TextInput(attrs={'class': "form-control",'type':'password'}))
    email = forms.EmailField(required=True,widget=forms.TextInput(attrs={'class': "form-control",'type':'email'}))

    

class UserDataForm(ModelForm):
    class Meta:
        model = UserData
        fields = ['t_factor','projects','trainings','leaves','status']

    t_factor = forms.DecimalField(max_digits=3, decimal_places=2, required=True, widget=forms.TextInput(attrs={'class': "form-control input-sm",'type':'number','step':"0.01"}))
    projects = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control input-sm",'type':'text'}))
    trainings = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control input-sm",'type':'text'}))
    leaves = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control input-sm",'type':'text','placeholder':'dd/mm/yyyy'}))
    status = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control input-sm",'type':'text'}))


class UserProjectForm(ModelForm):
    class Meta:
        model = UserData
        fields = ['username','project1','project2','project3','project4','project5','project6','project7','project8','project9','project10']

    username = forms.IntegerField(label='Username:',widget=forms.TextInput(attrs={'class': "form-control ",'type':'number','readonly':True}))
    project1 = forms.CharField(label='Project1:', required=False,widget=forms.TextInput(attrs={'class': "form-control input-sm",'type':'text'}))
    project2 = forms.CharField(label='Project2:', required=False,widget=forms.TextInput(attrs={'class': "form-control input-sm",'type':'text'}))
    project3 = forms.CharField(label='Project3:', required=False,widget=forms.TextInput(attrs={'class': "form-control input-sm",'type':'text'}))
    project4 = forms.CharField(label='Project4:', required=False,widget=forms.TextInput(attrs={'class': "form-control input-sm",'type':'text'}))
    project5 = forms.CharField(label='Project5:', required=False,widget=forms.TextInput(attrs={'class': "form-control input-sm",'type':'text'}))
    project6 = forms.CharField(label='Project6:', required=False,widget=forms.TextInput(attrs={'class': "form-control input-sm",'type':'text'}))
    project7 = forms.CharField(label='Project7:', required=False,widget=forms.TextInput(attrs={'class': "form-control input-sm",'type':'text'}))
    project8 = forms.CharField(label='Project8:', required=False,widget=forms.TextInput(attrs={'class': "form-control input-sm",'type':'text'}))
    project9 = forms.CharField(label='Project9:', required=False,widget=forms.TextInput(attrs={'class': "form-control input-sm",'type':'text'}))
    project10 = forms.CharField(label='Project10:', required=False,widget=forms.TextInput(attrs={'class': "form-control input-sm",'type':'text'}))


class SearchUserForm(ModelForm):
    class Meta:
        model = UserData
        fields = ['username']
    
    username = forms.IntegerField(label='Username:', required=True,widget=forms.TextInput(attrs={'class': "form-control ",'type':'number'}))