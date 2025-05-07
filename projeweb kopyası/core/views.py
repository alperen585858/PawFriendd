from django.shortcuts import render
from .models import Pet
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import JsonResponse
from config.database import Database
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.

def home(request):
    pets = Pet.objects.filter(status='available')[:6]
    return render(request, 'core/home.html', {'pets': pets})

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
def example_crud(request):
    db = Database()
    
    if request.method == 'POST':
        # Create a new record
        data = json.loads(request.body)
        try:
            result = db.insert_data('your_table_name', data)
            return JsonResponse({'status': 'success', 'data': result})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
            
    elif request.method == 'GET':
        # Get all records or a specific record
        record_id = request.GET.get('id')
        try:
            if record_id:
                result = db.select_by_id('your_table_name', int(record_id))
            else:
                result = db.select_all('your_table_name')
            return JsonResponse({'status': 'success', 'data': result})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
            
    elif request.method == 'PUT':
        # Update a record
        data = json.loads(request.body)
        record_id = data.pop('id', None)
        if not record_id:
            return JsonResponse({'status': 'error', 'message': 'ID is required'})
        try:
            result = db.update_by_id('your_table_name', record_id, data)
            return JsonResponse({'status': 'success', 'data': result})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
            
    elif request.method == 'DELETE':
        # Delete a record
        record_id = request.GET.get('id')
        if not record_id:
            return JsonResponse({'status': 'error', 'message': 'ID is required'})
        try:
            result = db.delete_by_id('your_table_name', int(record_id))
            return JsonResponse({'status': 'success', 'data': result})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
