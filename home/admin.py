# Import

from django.contrib import admin

# Import Data Sets from models.py
'''from home.models import Ingredients     # imports Ingredients table from models.py'''
'''from home.models import Tags            # imports tags table from models.py'''
from home.models import Interaction        # imports Interactions table from models.py
from home.models import InteractionType

# Import Basic Models from models.py
from home.models import CustomUser      # imports user table from models table
from home.models import Recipe          # imports recipe table from models table

# Import Junction Models from models.py
from home.models import Followers
from home.models import RecipeHistory
'''from home.models import RecipeIngredient'''
'''from home.models import RecipeTags
from home.models import Actions'''

# Register your models here.

# Register Data sets from modesl.py
'''admin.site.register(Ingredients)'''
'''admin.site.register(Tags)'''
admin.site.register(Interaction)

# Register Basic Models from models.py
admin.site.register(CustomUser)
admin.site.register(Recipe) 

# Register Junction Models from models.py
admin.site.register(Followers)
'''admin.site.register(RecipeTags)'''
admin.site.register(RecipeHistory)
'''admin.site.register(RecipeIngredient)'''
'''admin.site.register(Actions)'''