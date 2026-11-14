# Imports needed for "all views"
from django.template.response import TemplateResponse
from django.shortcuts import redirect, get_object_or_404
from rest_framework import status
from django.contrib.auth.decorators import login_required
from home.models import Interaction, InteractionType
from django.shortcuts import render

# Imports
from home.models import Recipe
from django.utils import timezone
from datetime import timedelta
from home.utils import expire_promotions
from .forms import RecipeForm, IngredientFormSet, StepFormSet, TagFormSet
from django.db import IntegrityError

# Recipe Edit -- Mike
@login_required # Only users with accounts can edit/post recipes
def recipe_edit(request, arg = None):
    
    recipe = get_object_or_404(Recipe, pk=arg) if arg else None # Get the recipe object if editing an existing one
    if request.method == 'POST':
        # If editing, pass instance; if creating, None
        form = RecipeForm(request.POST, instance=recipe)
        formset_ingredients = IngredientFormSet(request.POST, instance=recipe)
        formset_steps = StepFormSet(request.POST, instance=recipe)
        formset_tags = TagFormSet(request.POST, instance=recipe)
        image_data_uri = request.POST.get('image_data_uri')

        if form.is_valid() and formset_ingredients.is_valid() and formset_steps.is_valid() and formset_tags.is_valid():

            try:
                # Save the main recipe form, but don't commit to the database yet
                recipe = form.save(commit=False)
                print("Form saved with commit=False.")

                # --- Assign the user for new recipes ---
                # Check if this is a new recipe (instance does not have a primary key yet)
                if not recipe.pk:
                    recipe.user = request.user # Assign the currently logged-in user
                    print(f"Assigned user {request.user.username} to new recipe.")
                # --- End Assign user ---

                # Assign the Data URI string to the model field
                recipe.image = image_data_uri
                print("Image Data URI assigned to recipe instance.")

                # Save the recipe instance to the database
                recipe.save()
                print("Recipe instance saved to database.")

                # Save formsets with the now-saved recipe instance
                formset_ingredients.instance = recipe
                formset_ingredients.save()
                print("Ingredient formset saved.")

                formset_steps.instance = recipe
                formset_steps.save()
                print("Step formset saved.")

                formset_tags.instance = recipe
                formset_tags.save()
                print("Tag formset saved.")

                print("All save operations completed successfully.")

                # Redirect to the recipe page after successful save
                return redirect('/', pk=recipe.pk) # Not currently implemented

            except IntegrityError as e:
                # Catch database integrity errors
                print(f"Database Integrity Error during save: {e}")
                form.add_error(None, "A database error occurred. Please check your input.")
                # Fall through to render the template with errors

            except Exception as e:
                # Catch any other unexpected errors during the save process
                print(f"An unexpected error occurred during save: {e}")
                # Add a generic error message
                form.add_error(None, "An unexpected error occurred while saving. Please try again.")
                # Fall through to render the template with errors

    else:
        form = RecipeForm(instance=recipe)
        formset_ingredients = IngredientFormSet(instance=recipe)
        formset_steps = StepFormSet(instance=recipe)
        formset_tags = TagFormSet(instance=recipe)

    return TemplateResponse(request, 'recipe_edit.html', {
        'form': form,
        'formset_ingredients': formset_ingredients,
        'formset_steps': formset_steps,
        'formset_tags': formset_tags,
        'recipe': recipe
    })

def recipe_view(request, arg = None):
    """ View a recipe :) """
    recipe = get_object_or_404(Recipe, pk=arg)  # Get the recipe object from the database

    ingredients = recipe.ingredient_set.all()
    steps = recipe.step_set.all()
    tags = recipe.tag_set.all()

    # Check if the user has interacted with the recipe
    user = request.user
    like_status = False #default values
    bookmark_status = False
    if user.is_authenticated:
        like_status = Interaction.objects.filter(user=user, recipe=recipe, interaction_type=InteractionType.LIKE).exists()
        bookmark_status = Interaction.objects.filter(user=user, recipe=recipe, interaction_type=InteractionType.BOOKMARK).exists()


    # To show like counts on the recipe page. Like query - 5/12/2025 AJ
    like_count = Interaction.objects.filter(
        #recipe=recipe,
        interaction_type=InteractionType.LIKE
    ).count()

    return TemplateResponse(request, 'recipe_view.html', {
        'recipe': recipe,
        'ingredients': ingredients,
        'steps': steps,
        'tags': tags,
        'like_status': like_status,
        'bookmark_status': bookmark_status,
        'like_count': like_count
    }) # Pass the recipe object to the template



@login_required
def recipe_manage(request, arg = None):
    """ Manage your recipes; is a popup window showing options to edit, promote, hide, and delete a selected recipe. """

    # Authentication check and recipe retrieval
    print("recipe_manage triggered")            # Debugging
    user = request.user                         # Get the current user
    recipes = Recipe.objects.filter(user=user)  # Get all recipes created by the current user
    print("User recipes:", recipes)             # Debugging

    # Edit recipe
    if request.method == 'POST' and 'edit' in request.POST:         # Check if the edit button was clicked
        recipe_id = request.POST.get('recipe_id')                   # Get the recipe ID from the form data
        return redirect('recipe_edit', arg=recipe_id)               # Redirect to the recipe edit view for the selected recipe

    # Promote recipe
    if request.method == 'POST' and 'promote' in request.POST:      # Check if the promote button was clicked
        recipe_id = request.POST.get('recipe_id')                   # Get the recipe ID from the form data
        recipe = get_object_or_404(Recipe, pk=recipe_id)            # Get the recipe object from the database
        recipe.is_promoted = True                                   # Set the recipe as promoted
        recipe.promote_until = timezone.now() + timedelta(days=7)   # Set the promotion duration to 7 days
        expire_promotions()                                         # Call the function to expire promotions
        recipe.save()                                               # Save the changes to the database

    # Hide recipe
    if request.method == 'POST' and 'hide' in request.POST:         # Check if the hide button was clicked
        recipe_id = request.POST.get('recipe_id')                   # Get the recipe ID from the form data
        recipe = get_object_or_404(Recipe, pk=recipe_id)            # Get the recipe object from the database
        recipe.is_hidden = True                                     # Set the recipe as hidden
        recipe.save()                                               # Save the changes to the database

    # Delete recipe
    if request.method == 'POST' and 'delete' in request.POST:       # Check if the delete button was clicked
        recipe_id = request.POST.get('recipe_id')                   # Get the recipe ID from the form data
        recipe = get_object_or_404(Recipe, pk=recipe_id)            # Get the recipe object from the database
        recipe.delete()                                             # Delete the recipe from the database

    return TemplateResponse(request, 'recipe_manage.html')  