from django.contrib import admin
from .models import Pet, AdoptionApplication

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'breed', 'age', 'gender', 'status', 'created_at')
    list_filter = ('species', 'gender', 'status', 'is_vaccinated', 'is_neutered')
    search_fields = ('name', 'breed', 'description')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 20

@admin.register(AdoptionApplication)
class AdoptionApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'pet', 'status', 'created_at')
    list_filter = ('status', 'has_pets')
    search_fields = ('full_name', 'email', 'phone')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 20
