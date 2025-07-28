from supabase import create_client, Client
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_supabase_client(jwt: str = None) -> Client:
    """
    Create a Supabase client with optional JWT for user context.
    """
    client = create_client(SUPABASE_URL, SUPABASE_KEY)
    if jwt:
        client.postgrest.auth(jwt)
    return client