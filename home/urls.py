from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .views import search_all
from .views import toggle_interaction
from .views import toggle_interaction, interaction_test_view



urlpatterns = [
    path('', views.home, name='home'),
    path('test/', views.test, name='test'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('signup/', views.signup_view, name='signup'),
    path("upload/", views.upload_recipe, name="upload_recipe"),
    path('about/', views.about, name='about'),
    path('interact/<str:action_type>/', views.toggle_interaction, name='toggle_interaction'),
    path('search/', search_all, name='search_all'),                       # search thingy - AJ
    path('interaction-test/', interaction_test_view, name='interaction_test'),             # This is the test page for interaction toggle - http://localhost:8000/interaction-test/

]