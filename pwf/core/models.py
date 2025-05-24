from django.db import models
from django.contrib.auth.models import User

class Pet(models.Model):
    SPECIES_CHOICES = [
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('bird', 'Bird'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('available', 'Available for Adoption'),
        ('pending', 'Adoption Pending'),
        ('adopted', 'Adopted'),
    ]
    
    name = models.CharField(max_length=100, verbose_name='Name')
    species = models.CharField(max_length=50, choices=SPECIES_CHOICES, verbose_name='Species')
    breed = models.CharField(max_length=100, verbose_name='Breed')
    age = models.PositiveIntegerField(verbose_name='Age')
    gender = models.CharField(max_length=50, choices=[('male', 'Male'), ('female', 'Female')], verbose_name='Gender')
    description = models.TextField(verbose_name='Description')
    health_status = models.TextField(verbose_name='Health Status')
    is_vaccinated = models.BooleanField(default=False, verbose_name='Vaccinated')
    is_neutered = models.BooleanField(default=False, verbose_name='Neutered')
    photo = models.ImageField(upload_to='pets/', verbose_name='Photo', null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='available', verbose_name='Status')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Pet'
        verbose_name_plural = 'Pets'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class AdoptionApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Applicant')
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, verbose_name='Pet')
    full_name = models.CharField(max_length=150, verbose_name='Full Name')
    email = models.EmailField(verbose_name='Email')
    phone = models.CharField(max_length=20, verbose_name='Phone')
    address = models.TextField(verbose_name='Address')
    has_pets = models.BooleanField(default=False, verbose_name='Do you have other pets?')
    current_pets = models.TextField(blank=True, null=True, verbose_name='Current Pets')
    reason = models.TextField(verbose_name='Reason for Adoption')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending', verbose_name='Application Status')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Adoption Application'
        verbose_name_plural = 'Adoption Applications'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.full_name} - {self.pet.name}"

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

    class Meta:
        ordering = ['-created_at']
