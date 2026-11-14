# Imports
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings
from django.contrib.auth.models import PermissionsMixin
import bcrypt


class testImage(models.Model):
    imageURL = models.TextField(blank=True, null=True)


    # Django creates automatic ID for tables


# Custom made User model - AJ

class UserManager(BaseUserManager):
    """ User model with email, account creation date, and premium status. """
    # Will add password_hash, and profile_pic_url

    def create_user(self, email, password=None, **extra_fields):
        """ Creates and saves a User with the given email and password. """
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)

        # Sets username to email if not provided
        if not extra_fields.get("username"):
            extra_fields["username"] = email.split("@")[0]

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password, **extra_fields):
        """ Creates and saves a superuser with the given email and password. """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255, blank=False, null=False)  # blank and null are set to False to ensure password is required for user creation.
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    bio = models.TextField(blank=True, default="")  # Optional bio field
    created_at = models.DateTimeField(auto_now_add=True)
    profile_pic = models.CharField(max_length=255, blank=True, null=True)  # Optional profile picture
    is_premium = models.BooleanField(default=False)
    premium_since = models.DateTimeField(blank=True, null=True)  # Optional field to track when the user became premium
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    # Add bookmarked_user many to many relationship
    bookmarked_recipe = models.ManyToManyField(
        'home.Recipe',
        related_name='bookmarked_by',
        blank=True
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name', 'username']
   
   # Functions
    def set_password(self, raw_password):
        """
        Set the password for ther user and hash it using bcrypt.
        :param raw_password: The raw password to set.
        :return: None
        """
        if not raw_password:                                                                        # Ensure raw_password is provided before hashing
            raise ValueError("Password must be provided")                                           # Raise an error if no password is provided (not null or empty)
        hashed_password = bcrypt.hashpw(raw_password.encode('utf-8'), bcrypt.gensalt()).decode()    # Hash (and salt) the raw password using bcrypt
        if hashed_password is None:                                                                 # Ensure hashing was successful
            raise ValueError("Failed to hash password")                                             # Raise an error if hashing fails

        self.password = hashed_password

    def check_password(self, raw_password):
        """
        Check the raw password against the hashed password stored in the user instance for validation.
        :param raw_password: The raw password to check.
        :return: True if the password matches, False otherwise.
        """
        if not raw_password:                                                                # Ensure raw_password is provided (not null or empty)
            raise ValueError("Password must be provided")                                   # Raise an error if no password is provided
        if not self.password:                                                               # Ensure the user has a password set                
            return False
        return bcrypt.checkpw(raw_password.encode('utf-8'), self.password.encode('utf-8'))  # Check the raw password against the hashed password

    def __str__(self):
        """ Returns a string representation of the user. This is used when printing the user object. """
        return f"{self.first_name} {self.last_name} <{self.email}>"
    

# Updated Interaction related models - 5/1/2025 AJ

class InteractionType(models.TextChoices):
    """
    Keeps the interaction types here so we can share them with each other,
    and so people can't mess around and add more.
    
    Reminder: We only have 'like' and 'bookmark' — not 'favorite'.
    """

    LIKE = 'like' , 'Like'
    BOOKMARK = 'bookmark' , 'Bookmark'


class Interaction(models.Model):
    """
    Model for tracking interactions. 
    This replaces the old Action Model
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)      # user who did the action
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)      # the related recipe

    interaction_type = models.CharField(
        max_length=10,
        choices=InteractionType.choices,
        default=InteractionType.LIKE
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'recipe', 'interaction_type')
        # Apperantly the verbose stuff below tells Django how to display model's name on admin panel lol - AJ
        verbose_name = 'Interaction'
        verbose_name_plural ='Interactions'

    def __str__(self):
        # For easier debugging and admin display
        return f"{self.user} {self.interaction_type} {self.recipe}"
    

# Recipe Model to keep recipes in database, idk why I had to explain it... - AJ

class Recipe(models.Model):
    """Recipe model with title, user, description, recipe creation time, hidden, and promoted"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)                                        # Title of the recipe
    image = models.TextField(blank=False, null=False)                               # Image URL for the recipe (cannot be blank) 
    video = models.URLField(max_length = 500, blank=True, null=True)                # Optional video URL for the recipe (can be blank)
    description = models.TextField()                                                # Description of the recipe
    difficulty = models.CharField(max_length=50, default='', null=False)         # Difficulty of the recipe, null=False means it is required
    time = models.CharField(max_length=50, default=0)                               # Time required to prepare the recipe                                                      
    is_promoted = models.BooleanField(default=False)                                # Shows if the recipe is promoted
    promote_until = models.DateTimeField(blank=True, null=True)                     # Date until the recipe is promoted
    is_hidden = models.BooleanField(default=False)                                  # Shows if the recipe is hidden
    created_at = models.DateField(auto_now_add=True)                                # Date when the recipe is created

# Need to fix their relationships later.

# Ingredients, Steps, and Tags are implemented as formsets and as such need separate models - Mike
class Ingredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

class Step(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    text = models.TextField()

class Tag(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tagName = models.CharField(max_length=100)

class RecipeHistory(models.Model):
    """Stores the previous recipes"""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now_add=True)
    

# Unnecessarily complicated Followers Model to keep track of who's following who - AJ

class Followers(models.Model):
    """Followers model for keeping track of people following others"""
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='following',  # <== This is the fix
        on_delete=models.CASCADE
    )
    followed_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='followers',
        on_delete=models.CASCADE
    )
    followed_at =  models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'followed_user')

# pylint: disable=no-member

    def __str__(self):
        return f"{self.user.first_name} follows {self.followed_user.first_name}"  # it should work because django





__all__ = ['CustomUser']


# Removed Ingredients, Tags, and Action stuff - 5/1/2025 AJ

'''class Ingredients(models.Model):
    """Model for storing ingredient names."""
    name = models.CharField(max_length=50)                  # Name of the ingredient'''
'''    
    def __str__(self) -> str:
        return str(self.name)'''

'''class Tags(models.Model):
    """Model for categorizing items using tags."""
    name = models.CharField(max_length=100)     # Name of the tag
    
    def __str__(self) -> str:
        return str(self.name)         '''       


'''class RecipeIngredient(models.Model):
    """Stores each recipe's added ingredients"""

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
    quantity = models.FloatField(max_length=5)'''

'''class RecipeTags(models.Model):
    """Stores each recipe's tags"""

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE)'''

'''class Actions(models.Model):
    """It is and activity log"""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)
    interactions = models.ForeignKey('Interactions', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'recipe', 'interactions')         # so there won't be duplicates'''