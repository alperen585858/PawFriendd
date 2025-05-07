from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .auth import signup_user, signin_user, signout_user, auth_required
import json

@csrf_exempt
@require_http_methods(["POST"])
def signup(request):
    """
    Handle user signup
    """
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        metadata = data.get('metadata', {})

        if not email or not password:
            return JsonResponse({
                'error': 'Email and password are required'
            }, status=400)

        response = signup_user(email, password, metadata)
        return JsonResponse({
            'message': 'User created successfully',
            'data': response
        })
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=400)

@csrf_exempt
@require_http_methods(["POST"])
def signin(request):
    """
    Handle user signin
    """
    try:
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return JsonResponse({
                'error': 'Email and password are required'
            }, status=400)

        response = signin_user(email, password)
        return JsonResponse({
            'message': 'User signed in successfully',
            'data': response
        })
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=400)

@csrf_exempt
@require_http_methods(["POST"])
@auth_required
def signout(request):
    """
    Handle user signout
    """
    try:
        auth_header = request.headers.get('Authorization')
        token = auth_header.split(' ')[1] if auth_header else None

        if not token:
            return JsonResponse({
                'error': 'No authentication token provided'
            }, status=401)

        signout_user(token)
        return JsonResponse({
            'message': 'User signed out successfully'
        })
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=400)

@csrf_exempt
@require_http_methods(["GET"])
@auth_required
def me(request):
    """
    Get current user info
    """
    try:
        return JsonResponse({
            'user': request.user
        })
    except Exception as e:
        return JsonResponse({
            'error': str(e)
        }, status=400) 