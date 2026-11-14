from django import forms
from home.models import Recipe, CustomUser, Ingredient, Step, Tag
from django.forms import inlineformset_factory, Textarea

# Generates the formsets for the recipe model
# These formsets are used to create and edit the recipe model in the recipe_edit view
# Users can dynammically add and remove ingredients, steps, and tags
IngredientFormSet = inlineformset_factory(
    Recipe, Ingredient,
    fields=('name',),
    widgets={'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Ingredient'})},
    extra=1,
    can_delete=True
)
StepFormSet = inlineformset_factory(
    Recipe, Step,
    fields=('text',),
    widgets={'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter step details'})},
    extra=1,
    can_delete=True
)
TagFormSet = inlineformset_factory(
    Recipe, Tag,
    fields=('tagName',),
    widgets={'tagName': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Tag'})},
    extra=1,
    can_delete=True
)

# Define difficulty choices (Using integers as values)
DIFFICULTY_CHOICES = [
    (1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')
]

class RecipeForm(forms.ModelForm):
    difficulty = forms.ChoiceField(
        choices=DIFFICULTY_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'star-rating-input'}) # Class for input wrapper if needed, star styling is on label
        # The actual stars are handled by labels in the template now
    )

    # Use Textarea widget for description
    description = forms.CharField(widget=Textarea(attrs={'class': 'form-control', 'rows': 5}))

    class Meta:
        model = Recipe
        # Renamed 'time' to 'time_to_make' to match template/model image context
        fields = ['title', 'time', 'difficulty', 'description', 'video']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Recipe Title'}),
            # Consider a more specific widget if time needs units (e.g., NumberInput + Select)
            'time': forms.NumberInput(attrs={'min': '0', 'step': '1', 'class': 'form-control'}),
            # Description widget defined above
            'video': forms.ClearableFileInput(attrs={'class': 'form-control form-control-file'}), # Added form-control
        }
        labels = {
            'title': 'Recipe Title',
            'time': 'Time to make (Minutes)', # Updated label
            'difficulty': 'Difficulty', # Label handled in template now
            'description': 'Description',
            'video': 'Recipe Video', # Changed label
        }

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'bio']  # fields to be included in the form
        widgets = {  # widgets for the fields
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
        }
        labels = {  # labels for the fields
            'username': 'Username',
            'bio': 'bio',
        }

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password'
    }))

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }
