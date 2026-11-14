"""
The utils module. Contains helper functions for the app and Mayah didn't know where else to put this stuff.
"""
from django.utils import timezone
from .models import CustomUser, Recipe

def get_or_create_root_user():
    """ Get or create the root user with default credentials. FOR DEBUG PURPOSES ONLY. Delete during production. """
    root_email = "root@potluck.com"
    
    root_user, created = CustomUser.objects.get_or_create(
        email=root_email,
        defaults={
            "first_name": "Root",
            "last_name": "User",
            "is_staff": True,
            "is_superuser": True,
            "password": "temporarypassword"  # This will be overridden by .set_password()
        }
    )
    
    if created:
        root_user.set_password("temporarypassword")
        root_user.save()
    
    return root_user

def expire_promotions():
    """ Unpromotes all recipes whose promote_until date has passed. """
    now = timezone.now()
    expired_recipes = Recipe.objects.filter(is_promoted=True, promote_until__lt=now)
    for recipe in expired_recipes:
        recipe.is_promoted = False
        recipe.promote_until = None
        recipe.save()  # Save the changes to the database

    return expired_recipes.count()  # Return the number of expired promotions for debugging purposes (making sure it works)

def cancel_premium(user):
    """ Cancels a user's premium subscription and disables features. """
    user.is_premium = False
    user.premium_since = None
    user.save()