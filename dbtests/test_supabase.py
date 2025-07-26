#!/usr/bin/env python3
"""
Test script to verify Supabase connection
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_supabase_connection():
    try:
        from supabase import create_client, Client
        
        # Get credentials from environment
        SUPABASE_URL = os.getenv("SUPABASE_URL")
        SUPABASE_KEY = os.getenv("SUPABASE_KEY")
        
        if not SUPABASE_URL or not SUPABASE_KEY:
            print("❌ Missing Supabase credentials in .env file")
            print("Please set SUPABASE_URL and SUPABASE_KEY in your .env file")
            return False
        
        # Create client
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        print("✅ Supabase client created successfully")
        
        # Test connection by querying subscription_plans table
        response = supabase.table('subscription_plans').select("*").execute()
        print(f"✅ Successfully connected to Supabase!")
        print(f"✅ Found {len(response.data)} subscription plans")
        
        if response.data:
            for plan in response.data:
                print(f"   - Plan: {plan['name']} (${plan['price_monthly']}/month)")
        
        return True
        
    except Exception as e:
        print(f"❌ Supabase connection failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing Supabase connection...")
    test_supabase_connection()
