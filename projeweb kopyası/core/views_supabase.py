from django.shortcuts import render
from django.http import JsonResponse
from config.database import Database
from config.supabase import supabase
from django.views.decorators.csrf import csrf_exempt
import json

db = Database()

def home(request):
    # Get 6 available pets
    try:
        pets = db.custom_query('pets', 
            supabase.table('pets')
            .select('*')
            .eq('status', 'available')
            .limit(6)
            .order('created_at', desc=True)
        )
        return render(request, 'core/home.html', {'pets': pets})
    except Exception as e:
        return render(request, 'core/home.html', {'pets': [], 'error': str(e)})

def pets_list(request):
    try:
        # Start with base query
        query = supabase.table('pets').select('*').eq('status', 'available')
        
        # Search functionality
        search_query = request.GET.get('search', '')
        if search_query:
            query = query.or_(f"name.ilike.%{search_query}%,breed.ilike.%{search_query}%,description.ilike.%{search_query}%")
        
        # Filtering
        species = request.GET.get('species', '')
        gender = request.GET.get('gender', '')
        age = request.GET.get('age', '')
        is_vaccinated = request.GET.get('is_vaccinated', '')
        is_neutered = request.GET.get('is_neutered', '')
        
        if species:
            query = query.eq('species', species)
        if gender:
            query = query.eq('gender', gender)
        if age:
            if age == 'puppy':
                query = query.lte('age', 1)
            elif age == 'young':
                query = query.gt('age', 1).lte('age', 3)
            elif age == 'adult':
                query = query.gt('age', 3)
        if is_vaccinated:
            query = query.eq('is_vaccinated', True)
        if is_neutered:
            query = query.eq('is_neutered', True)
        
        # Sorting
        sort = request.GET.get('sort', '-created_at')
        if sort == 'name':
            query = query.order('name')
        elif sort == '-name':
            query = query.order('name', desc=True)
        elif sort == 'age':
            query = query.order('age')
        elif sort == '-age':
            query = query.order('age', desc=True)
        else:
            query = query.order('created_at', desc=True)
        
        # Execute query
        pets = db.custom_query('pets', query)
        
        # Manual pagination (Supabase doesn't support Django-style pagination)
        page = int(request.GET.get('page', 1))
        per_page = 9
        start = (page - 1) * per_page
        end = start + per_page
        
        paginated_pets = pets[start:end]
        total_pets = len(pets)
        
        context = {
            'pets': paginated_pets,
            'search_query': search_query,
            'selected_species': species,
            'selected_gender': gender,
            'selected_age': age,
            'selected_vaccinated': is_vaccinated,
            'selected_neutered': is_neutered,
            'selected_sort': sort,
            'view_type': request.GET.get('view', 'grid'),
            'species_choices': [('dog', 'Dog'), ('cat', 'Cat'), ('bird', 'Bird'), ('other', 'Other')],
            'total_pets': total_pets,
            'has_previous': page > 1,
            'has_next': end < total_pets,
            'page': page,
        }
        
        return render(request, 'core/pets_list.html', context)
    except Exception as e:
        return render(request, 'core/pets_list.html', {'error': str(e)})

@csrf_exempt
def pet_crud(request):
    db = Database()
    
    if request.method == 'POST':
        data = json.loads(request.body)
        try:
            result = db.insert_data('pets', data)
            return JsonResponse({'status': 'success', 'data': result})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    elif request.method == 'GET':
        pet_id = request.GET.get('id')
        try:
            if pet_id:
                result = db.select_by_id('pets', int(pet_id))
            else:
                result = db.select_all('pets')
            return JsonResponse({'status': 'success', 'data': result})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    elif request.method == 'PUT':
        data = json.loads(request.body)
        pet_id = data.pop('id', None)
        if not pet_id:
            return JsonResponse({'status': 'error', 'message': 'ID is required'})
        try:
            result = db.update_by_id('pets', pet_id, data)
            return JsonResponse({'status': 'success', 'data': result})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    elif request.method == 'DELETE':
        pet_id = request.GET.get('id')
        if not pet_id:
            return JsonResponse({'status': 'error', 'message': 'ID is required'})
        try:
            result = db.delete_by_id('pets', int(pet_id))
            return JsonResponse({'status': 'success', 'data': result})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}) 