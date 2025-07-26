#!/usr/bin/env python3
"""
Simple test to check if MongoDB is running and accessible
"""
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

async def check_mongodb():
    try:
        from motor.motor_asyncio import AsyncIOMotorClient
        
        MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
        
        print(f"Testing MongoDB connection to: {MONGODB_URI}")
        
        client = AsyncIOMotorClient(MONGODB_URI)
        
        # Simple ping test
        await client.admin.command('ping')
        print("✅ MongoDB is running and accessible!")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        print("\n💡 To fix this:")
        print("1. Install MongoDB: https://www.mongodb.com/try/download/community")
        print("2. Start MongoDB service")
        print("3. Or use MongoDB Atlas (cloud): https://www.mongodb.com/atlas")
        return False

if __name__ == "__main__":
    asyncio.run(check_mongodb())
