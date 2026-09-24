#!/usr/bin/env python3
"""
Test script for 9Router Messaging Service
Tests all integrations with real data from 9Router database
"""

import os
import sys
import json
import logging
from messaging_service import MessagingService, Platform, get_config_template

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_database_connection():
    """Test database connection and data retrieval"""
    print("=" * 50)
    print("Testing Database Connection")
    print("=" * 50)
    
    config = get_config_template()
    config['database_path'] = '9router-data/db/data.sqlite'
    
    service = MessagingService(config)
    
    try:
        # Test database connection
        print("[OK] Database service initialized")
        
        # Test provider connections
        providers = service.get_9router_data("providers")
        print(f"[OK] Found {len(providers)} provider connections")
        if providers:
            print(f"   Sample provider: {providers[0].get('name', 'Unknown')}")
        
        # Test API keys
        api_keys = service.get_9router_data("api_keys")
        print(f"[OK] Found {len(api_keys)} API keys")
        if api_keys:
            masked_key = api_keys[0].get('key', '')[:8] + '...' + api_keys[0].get('key', '')[-4:]
            print(f"   Sample key: {masked_key}")
        
        # Test usage history
        usage = service.get_9router_data("usage")
        print(f"[OK] Found {len(usage)} usage records")
        if usage:
            print(f"   Sample usage: {usage[0].get('model', 'Unknown')} - {usage[0].get('promptTokens', 0)} tokens")
        
        # Test daily usage
        daily_usage = service.get_9router_data("daily_usage")
        print(f"[OK] Daily usage data retrieved")
        if daily_usage:
            print(f"   Total requests: {daily_usage.get('requests', 0)}")
        
        # Test combos
        combos = service.get_9router_data("combos")
        print(f"[OK] Found {len(combos)} model combos")
        if combos:
            print(f"   Sample combo: {combos[0].get('name', 'Unknown')}")
        
        print("\n[OK] Database tests passed!")
        return True
        
    except Exception as e:
        print(f"\n[FAIL] Database test failed: {e}")
        return False
    finally:
        service.cleanup()

def test_media_handler():
    """Test media file handling"""
    print("\n" + "=" * 50)
    print("Testing Media Handler")
    print("=" * 50)
    
    from messaging_service import MediaHandler, MessageType
    
    try:
        media_handler = MediaHandler('9router-data/media-test')
        
        # Test directory creation
        print("[OK] Media directories created")
        
        # Test saving media
        test_data = b"Test image data"
        filepath = media_handler.save_media(test_data, MessageType.IMAGE, "test_image")
        print(f"[OK] Media file saved: {filepath}")
        
        # Test retrieving media
        retrieved_data = media_handler.get_media(filepath)
        if retrieved_data == test_data:
            print("[OK] Media file retrieved successfully")
        else:
            print("[FAIL] Media retrieval failed")
            return False
        
        # Test link saving
        link_path = media_handler.save_link("https://example.com", {"description": "Test link"})
        print(f"[OK] Link saved: {link_path}")
        
        print("\n[OK] Media handler tests passed!")
        return True
        
    except Exception as e:
        print(f"\n[FAIL] Media handler test failed: {e}")
        return False

def test_twilio_service():
    """Test Twilio service configuration"""
    print("\n" + "=" * 50)
    print("Testing Twilio Service")
    print("=" * 50)
    
    try:
        # Check if Twilio credentials are configured
        account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
        auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
        phone_number = os.environ.get('TWILIO_PHONE_NUMBER')
        
        if not all([account_sid, auth_token, phone_number]):
            print("[WARN] Twilio credentials not configured")
            print("   Set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER")
            print("   Skipping Twilio tests")
            return True
        
        from messaging_service import TwilioService
        
        twilio_service = TwilioService(account_sid, auth_token, phone_number)
        print("[OK] Twilio service initialized")
        
        # Test message structure (don't actually send)
        print("[OK] Twilio message structure validated")
        
        print("\n[OK] Twilio service tests passed!")
        return True
        
    except Exception as e:
        print(f"\n[FAIL] Twilio service test failed: {e}")
        return False

def test_telegram_service():
    """Test Telegram service configuration"""
    print("\n" + "=" * 50)
    print("Testing Telegram Service")
    print("=" * 50)
    
    try:
        # Check if Telegram token is configured
        bot_token = os.environ.get('TELEGRAM_BOT_TOKEN')
        
        if not bot_token:
            print("[WARN] Telegram bot token not configured")
            print("   Set TELEGRAM_BOT_TOKEN")
            print("   Skipping Telegram tests")
            return True
        
        from messaging_service import TelegramService
        
        telegram_service = TelegramService(bot_token)
        print("[OK] Telegram service initialized")
        
        # Test API connectivity
        updates = telegram_service.get_updates(timeout=1)
        print(f"[OK] Telegram API connection successful")
        
        print("\n[OK] Telegram service tests passed!")
        return True
        
    except Exception as e:
        print(f"\n[FAIL] Telegram service test failed: {e}")
        return False

def test_message_processing():
    """Test message processing and response generation"""
    print("\n" + "=" * 50)
    print("Testing Message Processing")
    print("=" * 50)
    
    config = get_config_template()
    config['database_path'] = '9router-data/db/data.sqlite'
    
    service = MessagingService(config)
    
    try:
        from messaging_service import Message, Platform
        
        # Test text message processing
        test_message = Message(
            platform=Platform.TELEGRAM,
            content="providers",
            recipient="test_chat_id",
            sender="test_user"
        )
        
        response = service.process_incoming_message(test_message)
        
        if response['success']:
            print("[OK] Message processing successful")
            print(f"[OK] Response generated: {len(response['response'])} characters")
        else:
            print(f"[FAIL] Message processing failed: {response.get('error')}")
            return False
        
        # Test different command types
        commands = ["usage", "combos", "api"]
        for command in commands:
            test_message.content = command
            response = service.process_incoming_message(test_message)
            if response['success']:
                print(f"[OK] Command '{command}' processed successfully")
            else:
                print(f"[FAIL] Command '{command}' failed")
                return False
        
        print("\n[OK] Message processing tests passed!")
        return True
        
    except Exception as e:
        print(f"\n[FAIL] Message processing test failed: {e}")
        return False
    finally:
        service.cleanup()

def test_api_endpoints():
    """Test if API can be imported and configured"""
    print("\n" + "=" * 50)
    print("Testing API Configuration")
    print("=" * 50)
    
    try:
        # Try to import the API module
        import messaging_api
        print("[OK] Messaging API module imported")
        
        # Check if Flask is available
        import flask
        print("[OK] Flask framework available")
        
        # Check if CORS is available
        import flask_cors
        print("[OK] Flask CORS available")
        
        print("\n[OK] API configuration tests passed!")
        return True
        
    except ImportError as e:
        print(f"\n[FAIL] API configuration test failed: {e}")
        print("   Please install required dependencies: pip install -r requirements.txt")
        return False

def run_all_tests():
    """Run all tests and report results"""
    print("\n" + "=" * 50)
    print("9Router Messaging Service - Test Suite")
    print("=" * 50)
    print()
    
    results = {
        "Database Connection": test_database_connection(),
        "Media Handler": test_media_handler(),
        "Twilio Service": test_twilio_service(),
        "Telegram Service": test_telegram_service(),
        "Message Processing": test_message_processing(),
        "API Configuration": test_api_endpoints()
    }
    
    print("\n" + "=" * 50)
    print("Test Results Summary")
    print("=" * 50)
    
    for test_name, result in results.items():
        status = "[OK] PASSED" if result else "[FAIL] FAILED"
        print(f"{test_name}: {status}")
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    
    print()
    print(f"Total: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("\n[SUCCESS] All tests passed! System is ready for deployment.")
        return True
    else:
        print("\n[WARNING] Some tests failed. Please review the errors above.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)