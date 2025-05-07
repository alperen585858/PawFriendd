from django.conf import settings
from config.supabase import supabase
from django.http import JsonResponse
from functools import wraps
from jose import jwt
import json

def signup_user(email, password, metadata=None):
    """
    Sign up a new user with Supabase
    """
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": metadata
            } if metadata else None
        })
        return response
    except Exception as e:
        raise Exception(f"Error signing up user: {str(e)}")

def signin_user(email, password):
    """
    Sign in a user with Supabase
    """
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        return response
    except Exception as e:
        raise Exception(f"Error signing in user: {str(e)}")

def signout_user(jwt_token):
    """
    Sign out a user from Supabase
    """
    try:
        supabase.auth.sign_out()
        return True
    except Exception as e:
        raise Exception(f"Error signing out user: {str(e)}")

def verify_jwt_token(token):
    """
    Verify the JWT token from Supabase
    """
    try:
        # For Supabase, we need to verify against the JWT secret
        # The secret is the service role key without the JWT part
        jwt_secret = settings.SUPABASE_SERVICE_KEY.split('.')[1]
        
        # Decode the JWT token
        decoded = jwt.decode(
            token,
            jwt_secret,
            algorithms=["HS256"],
            options={
                "verify_sub": True,
                "verify_iat": True,
                "verify_exp": True,
                "verify_aud": False,  # Supabase uses different audience format
                "verify_iss": False,  # We'll verify the issuer manually
            }
        )
        
        # Verify it's a Supabase token
        if decoded.get('iss') != f"https://{settings.SUPABASE_URL}/auth/v1":
            return None
            
        return decoded
    except Exception as e:
        print(f"Token verification error: {str(e)}")
        return None

def auth_required(f):
    """
    Decorator to check if user is authenticated
    """
    @wraps(f)
    def decorated_function(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return JsonResponse({
                'error': 'No authentication token provided'
            }, status=401)
        
        token = auth_header.split(' ')[1]
        decoded = verify_jwt_token(token)
        
        if not decoded:
            return JsonResponse({
                'error': 'Invalid authentication token'
            }, status=401)
        
        # Add user info to request
        request.user_id = decoded.get('sub')
        request.user = decoded
        
        return f(request, *args, **kwargs)
    
    return decorated_function 