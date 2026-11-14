from django import forms
from django.contrib.auth.forms import UserCreationForm
from home.models import CustomUser  
from home.models import testImage
from home.models import Recipe

class testImageForm(forms.ModelForm):
    class Meta:
        model = testImage
        fields = ['imageURL']

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'username')

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'image', 'video']




        '''For search stuff - AJ'''
        
class SearchForm(forms.Form):
    q = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'placeholder': 'Search...',
            'class': 'form-control me-2 shadow-none',
            'type': 'search',
            'aria-label': 'Search'
        })
    )