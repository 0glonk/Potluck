from django.urls import path
from . import views
from . import views_premium
from . import views_recipe
from . import views_login
from . import views_forgotpw

urlpatterns = [
    # Premium / Promote
    path('premium/', views_premium.premium, name='premium'),
    path('premium_upgrade/', views_premium.premium_upgrade, name='premium_upgrade'),
    path('cancel_premium/', views_premium.cancel_premium, name='cancel_premium'),   # Cancels premium subscription – Mayah
    path('recipe/<int:arg>/', views_recipe.recipe_view, name='recipe_detail'),      # trying to make search bar thing work with the recipe stuff - AJ - Also with like counts on recipes 

    # Recipe
    path('recipe_manage/', views_recipe.recipe_manage, name='recipe_manage'),
    path('recipe_edit/', views_recipe.recipe_edit, name='recipe_edit'),
    

    # Login/out
    path('logout/', views_login.logout_view, name='logout'),                        # logs out the user – AJ
    path('logout_page/', views_login.logout_view, name='logout_page'),              # Shows logout message – AJ
    path('login/', views_login.login_view, name='login'),                           # For login stuff obviously – AJ

    # Forgot Password
    path('forgot_pw/', views_forgotpw.forgot_pw, name='forgot_pw'),   
    path('reset_password/<uidb64>/<token>/', views_forgotpw.reset_password, name='reset_pw'), # Reset password page - Daniel                 

    # Settings and Profile
    #path('settings/', views.settings, name='settings'),
    #path('save_manage/', views.save_manage, name='save_manage'),
    path('edit_settings/', views.acct_settings, name='exact_settings'), # What is this? -Mayah
    path('user_profile/', views.user_profile, name='user_profile'),    # For the logged-in user to see their own user profile – AJ
    path('profile/<int:user_id>/', views.profile_visit, name='profile_visit'),  # Like /account/profile/3 – AJ
    path('update-profile/', views.update_profile, name='update_profile'), # For updating the user profile - Daniel
    path('sign_up/', views_login.sign_up, name='sign_up'),                                  # Sign up page - Daniel
                              
    # Email Stuff
    path('verify-email/<uidb64>/<token>/', views_login.verify_email, name='verify_email'),          # Email verification - Daniel 
    path('verify_email_sent/', views_login.email_verify_success, name='email_verify_sent'),         # Email verify success page - Daniel
    path('resend_email_link/', views_forgotpw.resend_email_link, name='resend_email_link'),         # Resend email link - Daniel

    # Trying to make queries work - 5/12/2025
    path('bookmarks/', views.bookmarks_view, name='bookmarks')                              # Bookmark query to bookmark.html? hopefully works...

]