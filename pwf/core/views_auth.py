from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import json

@csrf_exempt
@require_http_methods(["POST"])
def signup(request):
    """
    Handle user signup using Django's auth system
    """
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return JsonResponse({
                'error': 'Email and password are required'
            }, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({
                'error': 'Email already exists'
            }, status=400)

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )

        return JsonResponse({
            'message': 'User created successfully',
            'data': {
                'id': user.id,
                'email': user.email
            }
        })
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def signin(request):
    """
    Handle user signin using Django's auth system
    """
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return JsonResponse({
                'error': 'Email and password are required'
            }, status=400)

        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            return JsonResponse({
                'message': 'User signed in successfully',
                'data': {
                    'id': user.id,
                    'email': user.email
                }
            })
        else:
            return JsonResponse({
                'error': 'Invalid credentials'
            }, status=401)
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=400)

@csrf_exempt
@require_http_methods(["POST"])
@login_required
def signout(request):
    """
    Handle user signout using Django's auth system
    """
    try:
        logout(request)
        return JsonResponse({
            'message': 'User signed out successfully'
        })
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=400)

@csrf_exempt
@require_http_methods(["GET"])
@login_required
def me(request):
    """
    Get current user info using Django's auth system
    """
    try:
        return JsonResponse({
            'user': {
                'id': request.user.id,
                'email': request.user.email,
                'username': request.user.username
            }
        })
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=400) 