#!/usr/bin/env python3
"""
Test script to verify the logger utility works correctly
"""
import sys
import os
from pathlib import Path

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_logger():
    """Test the logger utility functions"""
    try:
        from shared.utils.logger import (
            app_logger, 
            audit_logger, 
            log_user_action, 
            log_system_event, 
            log_error,
            get_app_logger
        )
        
        print("✅ Successfully imported logger utilities")
        
        # Test basic logging
        app_logger.info("Testing application logger")
        app_logger.warning("This is a warning message")
        app_logger.error("This is an error message")
        
        print("✅ Basic logging test completed")
        
        # Test utility functions
        log_user_action("user123", "login", {"ip": "192.168.1.1"})
        log_system_event("STARTUP", "Application started successfully")
        
        print("✅ Utility functions test completed")
        
        # Test custom logger
        custom_logger = get_app_logger("test_service")
        custom_logger.info("Custom logger test message")
        
        print("✅ Custom logger test completed")
        
        # Check if log files were created
        logs_dir = Path("logs")
        if logs_dir.exists():
            log_files = list(logs_dir.glob("*.log"))
            print(f"✅ Log directory created with {len(log_files)} log files:")
            for log_file in log_files:
                print(f"   - {log_file.name}")
        else:
            print("⚠️  No logs directory found")
        
        # Test error logging
        try:
            # Intentionally cause an error
            result = 1 / 0
        except Exception as e:
            log_error(e, "test_logger function")
            print("✅ Error logging test completed")
        
        print("\n🎉 All logger tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Logger test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing Logger Utility...")
    print("=" * 50)
    test_logger()
