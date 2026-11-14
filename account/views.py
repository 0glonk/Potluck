# Imports :D

# Imports needed for "all views"
from django.template.response import TemplateResponse
from django.shortcuts import redirect, get_object_or_404
from rest_framework import status
from django.contrib.auth.decorators import login_required

from home.models import CustomUser
from .forms import CustomUserForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

# Email imports
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render
from django.contrib.auth.models import User

# Email verification imports
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

# Queries
from home.models import Recipe, Interaction, InteractionType

'''
# Login connection stuff -AJ
# I had a bug that about not recieving POST request, to fix it I had to make sure these stuff is triggered. That's why I added debug things. 
    # Turns out I forget to put {}...
def login_view(request):
    """ Log in the user and redirect to the home page. """
    print("login_view triggered")

    if request.method == 'POST':
        email = request.POST.get('email')  
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)
        print("Authenticated user:", user)  # TEMP: for debugging

        if user is not None:
            django_login(request, user)
            return redirect('/')  # can be changed to whatever
        else:
            return TemplateResponse(request, 'login.html', {'error': 'Invalid email or password'})

    return TemplateResponse(request, 'login.html', {})

def sign_up(request):
    if request.method == 'POST': # Check if the form is submitted
        email = request.POST.get('email') # Get the email from the form data
        password = request.POST.get('password') # Get the password from the form data
        username = request.POST.get('username') # Get the username from the form data

        # Create the user but set 'is_active' to False until email is verified
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password)
        user.is_active = False
        user.save() # Save the user to the database

        # Generate email verification token
        token = default_token_generator.make_token(user) # Generate a token for email verification
        uid = urlsafe_base64_encode(force_bytes(user.pk)) # Encode the user ID

        # Create the verification link
        verification_link = request.build_absolute_uri(f'/verify-email/{uid}/{token}/') # Create the verification link

        # Send the verification email
        send_mail(
            'Verify your email',
            f'Click the link to verify your email: {verification_link}', # Email content
            'noreply@potluck.com', # From email
            [email], # To email
            fail_silently=False,
        )

        return render(request, 'sign_up_success.html', {'email': email}) # Render a success page
    
    return render(request, 'sign_up.html') # Render the sign-up form

def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64)) # Decode the user ID
        user = User.objects.get(pk=uid) # Get the user object
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):   # Handle exceptions
        user = None # If the user does not exist, set user to None

    if user is not None and default_token_generator.check_token(user, token): # Check if the token is valid
        user.is_active = True #     Set the user as active
        user.save() # Save the user to the database
        return HttpResponse('Email verified successfully! You can now log in.')
    else:
        return HttpResponse('Invalid or expired verification link.')

# Log out connection stuff -AJ
def logout_view(request, arg = None):
    """ Log out the user and redirect to the home page. """
    print("logout_view triggered")  # For debugging
    django_logout(request)          # To end the session
    return redirect('home')         # Redirect to home page after logout

def logout_page(request):
    return TemplateResponse(request, 'logout.html', {})  # renders the "You have been logged out" message
'''
    
'''
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def promote_recipe(request, recipe_id):
    """ Promote a recipe for a user. """

    user = request.user                             # Get the current user
    recipe = get_object_or_404(Recipe, pk=recipe_id)# Get the recipe object from the database
    if not user.is_premium:                         # Check if the user is premium
        return redirect('premium_upgrade.html')     # Redirect to the premium upgrade page if not premium (Unless option is not available for free users)
    now = timezone.now()                            # Get the current time

    # Check if still within the premium period
    premium_expiration = user.premium_since + timedelta(days=30)  # Calculate the premium expiration time (30 days from premium_since)
    if now > premium_expiration:                                  # If the current time is greater than the premium expiration time
        return redirect('premium_upgrade.html')                   # Redirect to the premium upgrade page so user can renew subscription
    
    # Count the number of promoted recipes for the user
    promoted_during_premium = Recipe.objects.filter(    # Get the count of promoted recipes for the user this month
        user=user,                                      # Filter by user
        is_promoted=True,                               # Filter by promoted recipes
        promote_until_isnull=False,                     # Filter by recipes that have a promotion end date
        promote_until__gte=user.premium_since,          # Filter by recipes that were promoted during the premium period
        promote_until_lte=premium_expiration            # Filter by recipes that were promoted before the premium expiration time
    ).count()

    if promoted_during_premium >= 3:
        return Response({"error": "You have reached the maximum number of promoted recipes for this month."}, status=status.HTTP_400_BAD_REQUEST)
    
    # Get Recipe object
    try:
        recipe = Recipe.objects.get(pk=recipe_id, user=user)  # Get the recipe object from the database
    except Recipe.DoesNotExist:
        return Response({"error": "Recipe not found."}, status=status.HTTP_404_NOT_FOUND)
    
    # Promote the recipe
    recipe.is_promoted = True
    recipe.promote_until = now + timedelta(days=7)  # Set the promotion duration to 7 days
    recipe.save()                                   # Save the changes to the database
    return Response({"message": "Recipe promoted successfully."}, status=status.HTTP_200_OK)
'''
    
'''
# Recipe Stuff - Mayah
@login_required # Only users with accounts can edit/post recipes
def recipe_edit(request, arg = None):
    """ Create a new recipe or edit an existing one. They're the same view."""
    print("recipe_edit triggered")                              # For debugging
    
    recipe = get_object_or_404(Recipe, pk=arg) if arg else None # Get the recipe object if editing an existing one
    if request.method == 'POST' and recipe:                     # If editing an existing recipe
        recipe_name = request.POST.get('recipe_name')               # Get the recipe name from the form data
        recipe_description = request.POST.get('recipe_description')
        recipe_difficulty = request.POST.get('recipe_difficulty')
        recipe_ingredients = request.POST.get('recipe_ingredients')
        recipe_steps = request.POST.get('recipe_steps')
        recipe_time = request.POST.get('recipe_time')

        # Update the existing recipe in the database
        recipe.title = recipe_name
        recipe.description = recipe_description
        recipe.difficulty = recipe_difficulty
        # recipe.ingredients = recipe_ingredients // idk how to refer to junction table
        recipe.steps = recipe_steps
        recipe.time = recipe_time
        recipe.save()
    
    # If the request method is POST and no recipe is provided, it means we're creating a new recipe
    elif request.method == 'POST':  # Creates a new recipe (not updating one)
        recipe_name = request.POST.get('recipe_name')
        recipe_description = request.POST.get('recipe_description')
        recipe_difficulty = request.POST.get('recipe_difficulty')
        #recipe_ingredients = request.POST.get('recipe_ingredients')
        recipe_steps = request.POST.get('recipe_steps')
        recipe_time = request.POST.get('recipe_time')

        # Save the new recipe to the database; works by creating a new instance of the Recipe model
        # and calling the save() method on it.
        new_recipe = Recipe(
            title=recipe_name,
            description=recipe_description,
            difficulty=recipe_difficulty,
            #ingredients=recipe_ingredients,
            steps=recipe_steps,
            time=recipe_time
        )
        new_recipe.save()      

    return TemplateResponse(request, 'recipe_edit.html')
'''
    
'''
def recipe_view(request, arg = None):
    """ View a recipe :) """
    recipe = get_object_or_404(Recipe, pk=arg)  # Get the recipe object from the database
    print("recipe_view triggered")              # Debugging
    if recipe is None:                          # If the recipe is not found, return a 404 error
        print("Recipe not found")               # Debugging
    print("Recipe found:", recipe)              # Debugging
    return TemplateResponse(request, 'recipe_view.html', {'recipe': recipe}) # Pass the recipe object to the template
'''

'''
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
    '''

  # Profile page connection stuff - AJ

from .forms import SignUpForm

@csrf_exempt
@login_required
def update_profile(request):
    if request.method == "POST":
        username = request.POST.get("username")
        bio = request.POST.get("bio")
        request.user.username = username
        request.user.bio = bio
        request.user.save()
        return JsonResponse({'status': 'success', 'username': username, 'bio': bio})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

@login_required # Added recipe page -- Mike
def user_profile(request):
    user = request.user
    user_recipes = Recipe.objects.filter(user=user)  # Get all recipes created by the current user 
    bookmarked_recipes = bookmarked_recipes = Recipe.objects.filter(
            interaction__user=request.user,
            interaction__interaction_type=InteractionType.BOOKMARK
        ).distinct() # Get all recipes bookmarked by the current user

    user_recipe_data = []
    for recipe in user_recipes:
        # Fetch tags
        tags = recipe.tag_set.all()

         # Check if the user has interacted with the recipe (like and bookmark)
        like_status = Interaction.objects.filter(user=user, recipe=recipe, interaction_type=InteractionType.LIKE).exists()
        bookmark_status = Interaction.objects.filter(user=user, recipe=recipe, interaction_type=InteractionType.BOOKMARK).exists()

        # Collect the data for this recipe
        recipe_info = {
            'recipe': recipe,
            'tags': tags,
            'like_status': like_status,
            'bookmark_status': bookmark_status,
        }

        user_recipe_data.append(recipe_info)

    bookmark_recipe_data = []
    for recipe in bookmarked_recipes:
        # Fetch tags
        tags = recipe.tag_set.all()

         # Check if the user has interacted with the recipe (like and bookmark)
        like_status = Interaction.objects.filter(user=user, recipe=recipe, interaction_type=InteractionType.LIKE).exists()
        bookmark_status = Interaction.objects.filter(user=user, recipe=recipe, interaction_type=InteractionType.BOOKMARK).exists()

        # Collect the data for this recipe
        recipe_info = {
            'recipe': recipe,
            'tags': tags,
            'like_status': like_status,
            'bookmark_status': bookmark_status,
        }

        bookmark_recipe_data.append(recipe_info)

    return TemplateResponse(request, 'user_profile.html', {
        'user_obj': user,
        'user_recipes': user_recipe_data,
        'bookmarked_recipes': bookmark_recipe_data
    })


def profile_visit(request, user_id):
    like_status = False #default values
    bookmark_status = False
    
    user_obj = get_object_or_404(CustomUser,id=user_id)         # Retrieves user object from database
    user_acc = request.user
    user_recipes = Recipe.objects.filter(user=user_obj)
    is_own_profile = user_obj.id == request.user.id             # Checks if the user is viewing their own profile (boolean)

    if is_own_profile:
        return redirect('user_profile')                         # Redirects to the user's own profile page
    
    user_recipe_data = []
    for recipe in user_recipes:
        # Fetch tags
        tags = recipe.tag_set.all()

          # Check if the user has interacted with the recipe (like and bookmark)
        if user_acc.is_authenticated:
            like_status = Interaction.objects.filter(user=user_acc, recipe=recipe, interaction_type=InteractionType.LIKE).exists()
            bookmark_status = Interaction.objects.filter(user=user_acc, recipe=recipe, interaction_type=InteractionType.BOOKMARK).exists()

        # Collect the data for this recipe
        recipe_info = {
            'recipe': recipe,
            'tags': tags,
            'like_status': like_status,
            'bookmark_status': bookmark_status,
        }

        user_recipe_data.append(recipe_info)
    return TemplateResponse(request, 'profile_visit.html', {
        'user_obj': user_obj,
        'is_own_profile': is_own_profile,
        'user_recipes': user_recipe_data
    })

def acct_settings(request, arg = None):
    return TemplateResponse(request, 'acct_settings.html')

def signup_view(request):
    form = SignUpForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('login')
    return render(request, 'sign_up.html', {'form': form})


"""
def save_manage(request, arg = None):
    return TemplateResponse(request, 'save_manage.html')

def settings(request, arg = None):
    return TemplateResponse(request, 'acct_settings.html')
"""


# To show Bookmark Query in the bookmarks.html -> the button says Favorites in the website - 5/12/2025 AJ
def bookmarks_view(request):
    if request.user.is_authenticated:
        bookmarked_recipes = Recipe.objects.filter(
            interaction__user=request.user,
            interaction__interaction_type=InteractionType.BOOKMARK
        ).distinct()
    else:
        bookmarked_recipes = []

    return render(request, 'account/bookmarks.html', {
        'bookmarked_recipes': bookmarked_recipes
    })