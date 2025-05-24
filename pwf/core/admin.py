from django.contrib import admin
from .models import Pet, AdoptionApplication, Contact

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'breed', 'age', 'gender', 'status')
    list_filter = ('species', 'gender', 'status', 'is_vaccinated', 'is_neutered')
    search_fields = ('name', 'breed', 'description')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 20

@admin.register(AdoptionApplication)
class AdoptionApplicationAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'pet', 'status', 'created_at')
    list_filter = ('status', 'has_pets', 'created_at')
    search_fields = ('full_name', 'email', 'phone')
    readonly_fields = ('created_at',)
    list_per_page = 20

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at',)
