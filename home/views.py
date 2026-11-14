# Imports
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from .models import testImage
from . import forms
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login
from home.models import CustomUser
from .forms import CustomUserCreationForm
from django.views.decorators.csrf import csrf_exempt
import random #for recipe card picking


# Need these for search function - AJ 
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth import get_user_model
from .models import Recipe
from .forms import SearchForm

# For Interaction toggle - 5/1/2025 AJ
from django.shortcuts import get_object_or_404
from home.models import Recipe, Interaction, InteractionType
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required           # Used for other things too
from django.views.decorators.csrf import csrf_exempt                # only will be used for testing
import json


# Change notes
    # Deleted old interaction toggle using old Action Model, added a new one using new Interaction Model - 5/1/2025 AJ
    # Added route for interaction toggle test - 5/1/2025 AJ


# Test for Interaction Toggle - AJ
def interaction_test_view(request):
    return render(request, "home/interaction_test.html")

# Test for cropper (I think...) - AJ
def test(request):
    imageURLs = testImage.objects.all()
    if request.method == 'POST':
        form = forms.testImageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = forms.testImageForm()
    return TemplateResponse(request, 'test.html', {'form': form, 'imageURLs': imageURLs})

def home(request, arg=None):
    ids = list(Recipe.objects.values_list('id', flat=True)) # Get all recipe IDs
    like_status = False #default values
    bookmark_status = False

    #get 6 random recipes IDs for slider
    if len(ids) >= 6:
        slide_ids = random.sample(ids, 6)
    else:
        slide_ids = ids  # fallback if fewer than 8 recipes exist
    
    random_slides = sorted(
        Recipe.objects.filter(id__in=slide_ids), # Get the recipes corresponding to the random IDs
        key=lambda x: slide_ids.index(x.id) # Random sort
    )

    # Get a random sample of 20 recipe IDs
    if len(ids) >= 20:
        random_ids = random.sample(ids, 20)
    else:
        random_ids = ids  # fallback if fewer than 20 recipes exist

    random_recipes = sorted(
        Recipe.objects.filter(id__in=random_ids), # Get the recipes corresponding to the random IDs
        key=lambda x: random_ids.index(x.id) # Random sort
    )

    user = request.user
    recipe_data = []
    for recipe in random_recipes:
        # Fetch tags
        tags = recipe.tag_set.all()

         # Check if the user has interacted with the recipe (like and bookmark)
        if user.is_authenticated:
            like_status = Interaction.objects.filter(user=user, recipe=recipe, interaction_type=InteractionType.LIKE).exists()
            bookmark_status = Interaction.objects.filter(user=user, recipe=recipe, interaction_type=InteractionType.BOOKMARK).exists()

        # Collect the data for this recipe
        recipe_info = {
            'recipe': recipe,
            'tags': tags,
            'like_status': like_status,
            'bookmark_status': bookmark_status,
        }

        recipe_data.append(recipe_info)

    return TemplateResponse(request, 'home.html', {'recipes': recipe_data, 'recipeSlides': random_slides}) # Pass the recipe data to the template

def about(request, arg=None):
    return TemplateResponse(request, 'about.html', {})

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

# AWS stuff for uploading recipes to S3 bucket (this is a separate view function)
import boto3                                                #AWS SDK for Python
from home.forms import RecipeForm                               # Import RecipeForm
from home.models import Recipe, CustomUser                      # Import Recipe model
from .utils import get_or_create_root_user                  # Import utility function to get or create the root user (for testing purposes)
#from django.contrib.auth.decorators import login_required  # Import login_required decorator

# AWS S3 settings
#from .aws_settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_STORAGE_BUCKET_NAME, AWS_S3_REGION_NAME

# S3 client
'''
s3 = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_S3_REGION_NAME
)
'''

#@login_required                   # Ensure the user is logged in to upload a recipe
def upload_recipe(request):
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():                                 # If the form works, proceed to save the recipe to the database
            recipe = form.save(commit=False)                # Create a recipe object without saving to the database
            recipe.user = CustomUser.objects.first()        # Testing purposes, will replace with actual user later (root)
            # recipe.user = request.user                    # Uncomment this line in production to assign the logged-in user to the recipe
            recipe.name = get_or_create_root_user()         # Ensure the recipe has a user associated with it, for now using the first user (root) for testing purposes
            '''
            # Upload image to AWS S3 and save the URL to the recipe model
            image_file = request.FILES.get("image")                             # Get image file
            if image_file:                                                      # If there is an image file, proceed
                s3_path = f"recipe-images/{image_file.name}"                    # Define the path in S3 where the image will be stored
                s3.upload_fileobj(image_file, AWS_STORAGE_BUCKET_NAME, s3_path) # Upload the image to S3
                recipe.image = s3_path                                          # Save the S3 path to the recipe model for future references
            '''
            # Wrap up and save recipe to the database
            recipe.save()                                                       # Saves recipe
            return render(request, "upload_success.html", {"form": form})       # Return a success message (future success pop-up goes here)

    else:
        form = RecipeForm()                                                     # If the form is not valid, return the form again with errors (Future error pop-up goes here)
    return render(request, "upload.html", {"form": form})                       # Render the upload form for the user to fill out

# Interaction Toggle - 5/1/2025 AJ
# Expanded Json resoponse for greater control over template rendering -- Mike 5/12/2025
@csrf_exempt                                                                    # Only use this temporarily during testing 
@login_required
def toggle_interaction(request, action_type):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            recipe_id = data.get("recipe_id")
            recipe = get_object_or_404(Recipe, id=recipe_id)
        except Exception:
            return JsonResponse({"error": "Invalid data"}, status=400)

        user = request.user

        if action_type not in InteractionType.values:
            return JsonResponse({"error": "Invalid interaction type"}, status=400)

        interaction, created = Interaction.objects.get_or_create(
            user=user,
            recipe=recipe,
            interaction_type=action_type
        )

        if not created:
            interaction.delete()

            # Update bookmarked_recipe if it's a bookmark
            if action_type == 'bookmark':
                user.bookmarked_recipe.remove(recipe)

            like_count = Interaction.objects.filter(recipe=recipe, interaction_type='like').count()
            return JsonResponse({f"is_{action_type}": False, "like_count": like_count})
        else:
            # Add to bookmarked_recipe if it's a bookmark
            if action_type == 'bookmark':
                user.bookmarked_recipe.add(recipe)

            like_count = Interaction.objects.filter(recipe=recipe, interaction_type='like').count()
            return JsonResponse({f"is_{action_type}": True, "like_count": like_count})

    return JsonResponse({"error": "Invalid request"}, status=400)


# Search Stuff - AJ

User = get_user_model()

def search_all(request):
    form = SearchForm(request.GET)
    recipe_results = Recipe.objects.none()
    user_results = User.objects.none()

    if form.is_valid():
        query = form.cleaned_data['q']
        recipe_results = Recipe.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(ingredient__name__icontains=query)
        ).distinct()

        user_results = User.objects.filter(
            Q(username__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        ).distinct()

    return render(request, 'search_results.html', {
        'form': form,
        'recipes': recipe_results,
        'users': user_results,
        'query': form.cleaned_data.get('q', '')
    })
