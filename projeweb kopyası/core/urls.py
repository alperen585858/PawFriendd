from django.urls import path
from . import views_supabase as views
from . import views_auth

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('our-pets/', views.pets_list, name='pets_list'),
    path('api/pets/', views.pet_crud, name='pet_crud'),
    
    # Authentication endpoints
    path('api/auth/signup/', views_auth.signup, name='signup'),
    path('api/auth/signin/', views_auth.signin, name='signin'),
    path('api/auth/signout/', views_auth.signout, name='signout'),
    path('api/auth/me/', views_auth.me, name='me'),
] 