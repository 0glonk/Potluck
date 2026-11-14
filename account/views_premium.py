# Imports needed for "all views"
from django.template.response import TemplateResponse
from django.shortcuts import redirect, get_object_or_404
from rest_framework import status
from django.contrib.auth.decorators import login_required

# Premiums and Promotions
from home.utils import cancel_premium
from home.models import Recipe
from django.utils import timezone
from datetime import timedelta
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

# Recipe Promotion
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def promote_recipe(request, recipe_id):
    """ Promote a recipe for a user. """

    user = request.user                                             # Get the current user
    recipe = get_object_or_404(Recipe, pk=recipe_id)                # Get the recipe object from the database
    if not user.is_premium:                                         # Check if the user is premium
        return redirect('premium_upgrade.html')                     # Redirect to the premium upgrade page if not premium (Unless option is not available for free users)
    now = timezone.now()                                            # Get the current time

    premium_expiration = user.premium_since + timedelta(days=30)    # Check if still within period & calculate the premium expiration time (30 days from premium_since)
    if now > premium_expiration:                                    # If the current time is greater than the premium expiration time
        return redirect('premium_upgrade.html')                     # Redirect to the premium upgrade page so user can renew subscription
    
    promoted_during_premium = Recipe.objects.filter(                # Get the count of promoted recipes for the user this month
        user=user,                                                  # Filter by user
        is_promoted=True,                                           # Filter by promoted recipes
        promote_until_isnull=False,                                 # Filter by recipes that have a promotion end date
        promote_until__gte=user.premium_since,                      # Filter by recipes that were promoted during the premium period
        promote_until_lte=premium_expiration                        # Filter by recipes that were promoted before the premium expiration time
    ).count()

    # If user used all promotions
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


# ============= Premium Suff ============= #

@login_required
def premium_upgrade(request, arg = None):
    """ View the premium upgrade page; edit payment method and cancel premium subscription. """
    user = request.user
    return TemplateResponse(request, 'premium_upgrade.html')

@login_required
def cancel_premium(request):
    """ Cancel the user's premium subscription and redirect to the premium page. """
    user = request.user
    if not user.is_premium:
        return redirect('premium.html')
    cancel_premium(user)
    return redirect('premium.html')

def premium(request, arg = None):
    """ View the premium page. """
    return TemplateResponse(request, 'premium.html')