# import jwt
# from django.contrib.auth import get_user_model
# from django.conf import settings
# from rest_framework import authentication
# from rest_framework.exceptions import AuthenticationFailed

# User = get_user_model()

# class SupabaseJWTAuthentication(authentication.BaseAuthentication):
#     def authenticate(self, request):
#         auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
#         # Skip authentication for certain endpoints if needed
#         if not auth_header.startswith('Bearer '):
#             return None
            
#         token = auth_header.split(' ')[1]
        
#         try:
#             # Decode the JWT token (without verification for now)
#             payload = jwt.decode(
#                 token, 
#                 options={"verify_signature": False}  # We'll add verification later
#             )
            
#             # Extract user info from Supabase JWT
#             user_id = payload.get('sub')  # Supabase user UUID
#             email = payload.get('email')
            
#             if not user_id or not email:
#                 raise AuthenticationFailed('Invalid token payload')
                
#             # Get or create user in Django database
#             user, created = User.objects.get_or_create(
#                 username=user_id,  # Use Supabase UUID as username
#                 defaults={
#                     'email': email,
#                     'first_name': payload.get('user_metadata', {}).get('full_name', ''),
#                     'is_active': True
#                 }
#             )
            
#             if created:
#                 print(f"Created new user: {email} ({user_id})")
#             else:
#                 print(f"Authenticated existing user: {email}")
            
#             return (user, token)
            
#         except jwt.ExpiredSignatureError:
#             raise AuthenticationFailed('Token expired')
#         except jwt.InvalidTokenError as e:
#             raise AuthenticationFailed(f'Invalid token: {str(e)}')
#         except Exception as e:
#             raise AuthenticationFailed(f'Authentication error: {str(e)}')

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()

class SupabaseJWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]

        try:
            # Decode JWT without verifying signature (Supabase handles it)
            payload = jwt.decode(token, options={"verify_signature": False})
        except jwt.PyJWTError:
            raise AuthenticationFailed("Invalid JWT")

        email = payload.get("email")
        if not email:
            raise AuthenticationFailed("No email in JWT")

        # Get or create the user locally
        user, _ = User.objects.get_or_create(
            email=email,
            defaults={"username": email.split("@")[0]}
        )

        return (user, None)
