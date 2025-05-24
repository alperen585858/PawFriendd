from django.shortcuts import render, get_object_or_404, redirect
from .models import Pet, AdoptionApplication, Contact
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json

# Create your views here.

def home(request):
    pets = Pet.objects.filter(status='available')[:6]
    return render(request, 'core/home.html', {'pets': pets})

@login_required
def pets_list(request):
    # Get all available pets
    pets = Pet.objects.filter(status='available')
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        pets = pets.filter(
            Q(name__icontains=search_query) |
            Q(breed__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Filtering
    species = request.GET.get('species', '')
    gender = request.GET.get('gender', '')
    age = request.GET.get('age', '')
    is_vaccinated = request.GET.get('is_vaccinated', '')
    is_neutered = request.GET.get('is_neutered', '')
    
    if species:
        pets = pets.filter(species=species)
    if gender:
        pets = pets.filter(gender=gender)
    if age:
        if age == 'puppy':
            pets = pets.filter(age__lte=1)
        elif age == 'young':
            pets = pets.filter(age__gt=1, age__lte=3)
        elif age == 'adult':
            pets = pets.filter(age__gt=3)
    if is_vaccinated:
        pets = pets.filter(is_vaccinated=True)
    if is_neutered:
        pets = pets.filter(is_neutered=True)
    
    # Sorting
    sort = request.GET.get('sort', '-created_at')
    if sort == 'name':
        pets = pets.order_by('name')
    elif sort == '-name':
        pets = pets.order_by('-name')
    elif sort == 'age':
        pets = pets.order_by('age')
    elif sort == '-age':
        pets = pets.order_by('-age')
    else:
        pets = pets.order_by('-created_at')
    
    # View type (grid/list)
    view_type = request.GET.get('view', 'grid')
    
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(pets, 9)  # Show 9 pets per page
    pets = paginator.get_page(page)
    
    context = {
        'pets': pets,
        'search_query': search_query,
        'selected_species': species,
        'selected_gender': gender,
        'selected_age': age,
        'selected_vaccinated': is_vaccinated,
        'selected_neutered': is_neutered,
        'selected_sort': sort,
        'view_type': view_type,
        'species_choices': Pet.SPECIES_CHOICES,
        'total_pets': paginator.count,
    }
    
    return render(request, 'core/pets_list.html', context)

@csrf_exempt
def pet_crud(request):
    if request.method == 'POST':
        # Create a new pet
        try:
            data = json.loads(request.body)
            pet = Pet.objects.create(**data)
            return JsonResponse({
                'status': 'success',
                'data': {
                    'id': pet.id,
                    'name': pet.name,
                    'species': pet.species,
                    'breed': pet.breed,
                    'age': pet.age,
                    'gender': pet.gender,
                    'status': pet.status
                }
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
            
    elif request.method == 'GET':
        # Get all pets or a specific pet
        pet_id = request.GET.get('id')
        try:
            if pet_id:
                pet = get_object_or_404(Pet, id=pet_id)
                data = {
                    'id': pet.id,
                    'name': pet.name,
                    'species': pet.species,
                    'breed': pet.breed,
                    'age': pet.age,
                    'gender': pet.gender,
                    'status': pet.status
                }
            else:
                pets = Pet.objects.all()
                data = [{
                    'id': pet.id,
                    'name': pet.name,
                    'species': pet.species,
                    'breed': pet.breed,
                    'age': pet.age,
                    'gender': pet.gender,
                    'status': pet.status
                } for pet in pets]
            return JsonResponse({'status': 'success', 'data': data})
        except Pet.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Pet not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
            
    elif request.method == 'PUT':
        # Update a pet
        try:
            data = json.loads(request.body)
            pet_id = data.pop('id', None)
            if not pet_id:
                return JsonResponse({'status': 'error', 'message': 'ID is required'})
            
            pet = get_object_or_404(Pet, id=pet_id)
            for key, value in data.items():
                setattr(pet, key, value)
            pet.save()
            
            return JsonResponse({
                'status': 'success',
                'data': {
                    'id': pet.id,
                    'name': pet.name,
                    'species': pet.species,
                    'breed': pet.breed,
                    'age': pet.age,
                    'gender': pet.gender,
                    'status': pet.status
                }
            })
        except Pet.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Pet not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
            
    elif request.method == 'DELETE':
        # Delete a pet
        pet_id = request.GET.get('id')
        if not pet_id:
            return JsonResponse({'status': 'error', 'message': 'ID is required'})
        try:
            pet = get_object_or_404(Pet, id=pet_id)
            pet.delete()
            return JsonResponse({'status': 'success', 'message': 'Pet deleted successfully'})
        except Pet.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Pet not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

def adoption_info(request):
    """View for general adoption information and process"""
    return render(request, 'core/adoption/info.html')

@login_required
def adoption_apply(request, pet_id):
    """View for submitting adoption application"""
    pet = get_object_or_404(Pet, id=pet_id, status='available')
    
    if request.method == 'POST':
        # Check if user already has a pending application for this pet
        if AdoptionApplication.objects.filter(user=request.user, pet=pet, status='pending').exists():
            messages.error(request, 'You already have a pending application for this pet.')
            return redirect('core:pets_list')
            
        application = AdoptionApplication(
            user=request.user,
            pet=pet,
            full_name=request.POST.get('full_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            has_pets=request.POST.get('has_pets') == 'on',
            current_pets=request.POST.get('current_pets'),
            reason=request.POST.get('reason')
        )
        application.save()
        
        # Update pet status
        pet.status = 'pending'
        pet.save()
        
        messages.success(request, 'Your adoption application has been submitted successfully!')
        return redirect('core:adoption_applications')
        
    return render(request, 'core/adoption/apply.html', {'pet': pet})

@login_required
def adoption_applications(request):
    """View for listing user's adoption applications"""
    applications = AdoptionApplication.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'core/adoption/applications.html', {'applications': applications})

def about_us(request):
    """View for About Us page"""
    return render(request, 'core/about_us.html')

def contact(request):
    """View for Contact page"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Save the contact message to database
        Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        
        messages.success(request, 'Thank you for your message! We will get back to you soon.')
        return redirect('core:contact')
        
    return render(request, 'core/contact.html')
