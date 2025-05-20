from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('our-pets/', views.pets_list, name='pets_list'),
    path('adoption/', views.adoption_info, name='adoption_info'),
    path('adoption/apply/<int:pet_id>/', views.adoption_apply, name='adoption_apply'),
    path('adoption/applications/', views.adoption_applications, name='adoption_applications'),
    path('api/pets/', views.pet_crud, name='pet_crud'),
] 