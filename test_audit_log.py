#!/usr/bin/env python3
"""
Test script to add audit logs to MongoDB
"""
import asyncio
import os
import uuid
from datetime import datetime, timezone
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_add_audit_log():
    try:
        from motor.motor_asyncio import AsyncIOMotorClient
        from shared.models.audit_log import AuditLog
        
        # Get MongoDB configuration
        MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
        MONGODB_DB = os.getenv("MONGODB_DB", "zubaschool")
        
        print(f"🔍 Connecting to MongoDB: {MONGODB_URI}")
        print(f"🔍 Database: {MONGODB_DB}")
        
        # Create client and connect to database
        client = AsyncIOMotorClient(MONGODB_URI)
        db = client[MONGODB_DB]
        
        # Test connection
        await client.admin.command('ping')
        print("✅ MongoDB connection successful!")
        
        # Create audit log collection reference
        audit_logs_collection = db.audit_logs
        
        # Create sample audit log entries (using string UUIDs and timezone-aware datetime)
        sample_logs = [
            {
                "tenant_id": str(uuid.uuid4()),
                "user_id": str(uuid.uuid4()),
                "action": "tenant_created",
                "details": {
                    "school_name": "Test School A",
                    "subscription_plan": "Pro",
                    "created_by": "system_admin"
                },
                "created_at": datetime.now(timezone.utc)
            },
            {
                "tenant_id": str(uuid.uuid4()),
                "user_id": str(uuid.uuid4()),
                "action": "user_login",
                "details": {
                    "username": "admin@testschool.com",
                    "ip_address": "192.168.1.100",
                    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                },
                "created_at": datetime.now(timezone.utc)
            },
            {
                "tenant_id": str(uuid.uuid4()),
                "user_id": str(uuid.uuid4()),
                "action": "subscription_updated",
                "details": {
                    "old_plan": "Basic",
                    "new_plan": "Pro",
                    "updated_by": "school_admin"
                },
                "created_at": datetime.now(timezone.utc)
            }
        ]
        
        print(f"\n📝 Adding {len(sample_logs)} audit log entries...")
        
        # Insert audit logs
        for i, log_data in enumerate(sample_logs, 1):
            # Validate using Pydantic model
            audit_log = AuditLog(**log_data)
            
            # Convert to dict for MongoDB insertion
            log_dict = audit_log.model_dump()
            
            # Insert into MongoDB
            result = await audit_logs_collection.insert_one(log_dict)
            print(f"✅ Audit log {i} inserted with ID: {result.inserted_id}")
            print(f"   Action: {log_data['action']}")
            print(f"   Details: {log_data['details']}")
        
        # Query and display all audit logs
        print(f"\n📋 Retrieving all audit logs from database...")
        cursor = audit_logs_collection.find({})
        logs = await cursor.to_list(length=100)
        
        print(f"✅ Found {len(logs)} audit log entries:")
        for i, log in enumerate(logs, 1):
            print(f"\n   Log {i}:")
            print(f"   - ID: {log['_id']}")
            print(f"   - Action: {log['action']}")
            print(f"   - Tenant ID: {log['tenant_id']}")
            print(f"   - User ID: {log['user_id']}")
            print(f"   - Created: {log['created_at']}")
            print(f"   - Details: {log['details']}")
        
        # Test querying by action
        print(f"\n🔍 Testing query by action 'tenant_created'...")
        tenant_creation_logs = await audit_logs_collection.find({"action": "tenant_created"}).to_list(length=10)
        print(f"✅ Found {len(tenant_creation_logs)} tenant creation logs")
        
        # Test querying by date range (last hour)
        one_hour_ago = datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0)
        recent_logs = await audit_logs_collection.find({
            "created_at": {"$gte": one_hour_ago}
        }).to_list(length=10)
        print(f"✅ Found {len(recent_logs)} logs from the last hour")
        
        # Close connection
        client.close()
        print(f"\n🎉 Audit log testing completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Audit log test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_shared_mongodb_audit():
    try:
        print(f"\n" + "="*60)
        print("Testing audit logs with shared MongoDB module...")
        
        from shared.database.mongodb import db
        from shared.models.audit_log import AuditLog
        
        # Create a test audit log
        test_log_data = {
            "tenant_id": str(uuid.uuid4()),
            "user_id": str(uuid.uuid4()),
            "action": "test_shared_module",
            "details": {
                "module": "shared.database.mongodb",
                "test_type": "audit_log_insertion"
            },
            "created_at": datetime.now(timezone.utc)
        }
        
        # Validate with Pydantic
        audit_log = AuditLog(**test_log_data)
        
        # Insert using shared module
        result = await db.audit_logs.insert_one(audit_log.model_dump())
        print(f"✅ Shared module test: Audit log inserted with ID: {result.inserted_id}")
        
        # Query it back
        retrieved_log = await db.audit_logs.find_one({"_id": result.inserted_id})
        print(f"✅ Shared module test: Retrieved log action: {retrieved_log['action']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Shared module audit test failed: {e}")
        return False

async def main():
    print("Testing MongoDB Audit Log Operations...")
    print("="*60)
    
    # Test direct MongoDB operations
    success1 = await test_add_audit_log()
    
    # Test shared module
    success2 = await test_shared_mongodb_audit()
    
    print("\n" + "="*60)
    if success1 and success2:
        print("🎉 All audit log tests passed!")
        print("✅ MongoDB is properly configured for audit logging")
    else:
        print("⚠️  Some audit log tests failed. Check your MongoDB configuration.")

if __name__ == "__main__":
    asyncio.run(main())
