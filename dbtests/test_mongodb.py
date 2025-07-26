#!/usr/bin/env python3
"""
Test script to verify MongoDB connection
"""
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_mongodb_connection():
    try:
        from motor.motor_asyncio import AsyncIOMotorClient
        
        # Get credentials from environment
        MONGODB_URI = os.getenv("MONGODB_URI")
        MONGODB_DB = os.getenv("MONGODB_DB", "zubaschool")
        
        if not MONGODB_URI:
            print("❌ Missing MongoDB URI in .env file")
            print("Please set MONGODB_URI in your .env file")
            return False
        
        print(f"🔍 Testing connection to: {MONGODB_URI}")
        print(f"🔍 Database: {MONGODB_DB}")
        
        # Create client
        client = AsyncIOMotorClient(MONGODB_URI)
        db = client[MONGODB_DB]
        print("✅ MongoDB client created successfully")
        
        # Test connection by pinging the server
        await client.admin.command('ping')
        print("✅ Successfully pinged MongoDB!")
        
        # Test database access
        collections = await db.list_collection_names()
        print(f"✅ Connected to database '{MONGODB_DB}'")
        print(f"✅ Found {len(collections)} collections")
        
        if collections:
            print("   Collections:")
            for collection in collections:
                count = await db[collection].count_documents({})
                print(f"   - {collection}: {count} documents")
        else:
            print("   No collections found (this is normal for a new database)")
        
        # Test creating a test collection and document
        test_collection = db.test_connection
        test_doc = {"test": True, "message": "MongoDB connection test successful"}
        result = await test_collection.insert_one(test_doc)
        print(f"✅ Test document inserted with ID: {result.inserted_id}")
        
        # Clean up test document
        await test_collection.delete_one({"_id": result.inserted_id})
        print("✅ Test document cleaned up")
        
        # Close connection
        client.close()
        print("✅ MongoDB connection test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
        return False

async def test_shared_mongodb():
    try:
        print("\n" + "="*50)
        print("Testing shared MongoDB module...")
        
        from shared.database.mongodb import db, mongo_client
        
        # Test ping
        await mongo_client.admin.command('ping')
        print("✅ Shared MongoDB module connection successful!")
        
        # Test database operations
        collections = await db.list_collection_names()
        print(f"✅ Database accessible through shared module")
        print(f"✅ Collections: {len(collections)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Shared MongoDB module test failed: {e}")
        return False

async def main():
    print("Testing MongoDB connection...")
    print("="*50)
    
    # Test direct connection
    success1 = await test_mongodb_connection()
    
    # Test shared module
    success2 = await test_shared_mongodb()
    
    print("\n" + "="*50)
    if success1 and success2:
        print("🎉 All MongoDB tests passed!")
    else:
        print("⚠️  Some MongoDB tests failed. Check your configuration.")

if __name__ == "__main__":
    asyncio.run(main())
