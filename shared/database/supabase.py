from supabase import create_client, Client
from ..config import SUPABASE_URL, SUPABASE_KEY

# Initialize Supabase client
supabase: Client = None

if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    print("Warning: Supabase credentials not found. Please check your .env file.")