# from supabase import create_client
# import os

# url = os.getenv("SUPABASE_URL")
# service_key = os.getenv("SUPABASE_KEY")

# supabase = create_client(url, service_key)

# def is_supabase_user(email: str) -> bool:
#     try:
#         normalized_email = email.strip().lower()
#         response = supabase.auth.admin.list_users()

#         # Debugging: show the first few emails from Supabase
#         users = response.users
#         print("🔎 Supabase returned", len(users), "users")
#         for u in users[:10]:  # just preview the first 10
#             print("   →", u.email)

#         # Now check if the given email exists
#         return any(u.email.lower() == normalized_email for u in users)

#     except Exception as e:
#         print("Supabase check error:", e)
#         return False

from supabase import create_client
from django.conf import settings

# Setup Supabase client
supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

def is_supabase_user(email: str) -> bool:
    try:
        normalized_email = email.strip().lower()
        response = supabase.auth.admin.list_users()  # returns list of User objects
        print("🔎 Raw Supabase response:", response)

        for user in response:
            user_email = getattr(user, "email", None)
            print("   → Checking user:", user_email)
            if user_email and user_email.strip().lower() == normalized_email:
                return True
        return False
    except Exception as e:
        print("Supabase check error:", e)
        return False
