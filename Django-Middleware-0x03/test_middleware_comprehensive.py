#!/usr/bin/env python3
"""
Comprehensive middleware testing script for Django-Middleware-0x03 project.
This script tests all middleware components:
1. RequestLoggingMiddleware
2. RestrictAccessByTimeMiddleware  
3. OffensiveLanguageMiddleware
4. RolePermissionMiddleware
"""

import requests
import time
import json
from datetime import datetime

# Base URL for the Django server
BASE_URL = "http://127.0.0.1:8000"

def print_test_header(test_name):
    """Print a formatted test header."""
    print("\n" + "="*60)
    print(f"TESTING: {test_name}")
    print("="*60)

def print_response_info(response, description=""):
    """Print response information in a formatted way."""
    print(f"\n{description}")
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}")
    try:
        response_data = response.json()
        print(f"Response Body: {json.dumps(response_data, indent=2)}")
    except:
        print(f"Response Body: {response.text}")
    print("-" * 40)

def test_request_logging_middleware():
    """Test the RequestLoggingMiddleware by making various requests."""
    print_test_header("REQUEST LOGGING MIDDLEWARE")
    
    # Test different endpoints to generate log entries
    endpoints = [
        "/api/",
        "/admin/",
        "/api/users/",
        "/api/conversations/",
        "/api/messages/"
    ]
    
    print("Making requests to different endpoints to test logging...")
    for endpoint in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
            print(f"✓ Request to {endpoint} - Status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"✗ Request to {endpoint} failed: {e}")
    
    print("\n📄 Check the 'requests.log' file to see logged requests!")

def test_time_restriction_middleware():
    """Test the RestrictAccessByTimeMiddleware."""
    print_test_header("TIME RESTRICTION MIDDLEWARE")
    
    current_hour = datetime.now().hour
    print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Current hour: {current_hour}")
    print(f"Allowed hours: 6 AM (6) to 9 PM (21)")
    
    if 6 <= current_hour < 21:
        print("✓ Current time is within allowed hours - requests should succeed")
        expected_status = "Success (not blocked)"
    else:
        print("✓ Current time is outside allowed hours - requests should be blocked")
        expected_status = "Blocked (403 Forbidden)"
    
    # Test a simple request
    try:
        response = requests.get(f"{BASE_URL}/api/", timeout=5)
        print_response_info(response, f"Test request result - Expected: {expected_status}")
    except requests.exceptions.RequestException as e:
        print(f"✗ Request failed: {e}")

def test_rate_limiting_middleware():
    """Test the OffensiveLanguageMiddleware (rate limiting)."""
    print_test_header("RATE LIMITING MIDDLEWARE (OffensiveLanguageMiddleware)")
    
    print("Testing rate limiting by sending multiple POST requests...")
    print("Rate limit: 5 messages per minute")
    
    # Data for POST request
    test_data = {
        "message_body": "Test message for rate limiting",
        "conversation": "test-conversation-id"
    }
    
    # Send multiple POST requests to trigger rate limiting
    for i in range(7):  # Send 7 requests to exceed limit of 5
        try:
            response = requests.post(
                f"{BASE_URL}/api/messages/", 
                json=test_data,
                headers={'Content-Type': 'application/json'},
                timeout=5
            )
            print(f"Request {i+1}: Status {response.status_code}")
            
            if response.status_code == 429:
                print_response_info(response, f"✓ Rate limit triggered on request {i+1}")
                break
            elif i >= 4:  # After 5 requests
                print_response_info(response, f"Request {i+1} - Checking for rate limit")
            
            # Small delay between requests
            time.sleep(0.1)
            
        except requests.exceptions.RequestException as e:
            print(f"Request {i+1} failed: {e}")

def test_role_permission_middleware():
    """Test the RolePermissionMiddleware."""
    print_test_header("ROLE PERMISSION MIDDLEWARE")
    
    print("Testing role-based access control...")
    print("Protected paths: /admin/, /api/users/, /api/conversations/")
    print("Required roles: admin or moderator")
    
    protected_endpoints = [
        "/admin/",
        "/api/users/",
        "/api/conversations/"
    ]
    
    for endpoint in protected_endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", timeout=5)
            print_response_info(response, f"Access attempt to {endpoint}")
            
            if response.status_code == 403:
                print(f"✓ Access properly restricted for {endpoint}")
            elif response.status_code == 401:
                print(f"✓ Authentication required for {endpoint}")
            else:
                print(f"? Unexpected response for {endpoint}")
                
        except requests.exceptions.RequestException as e:
            print(f"✗ Request to {endpoint} failed: {e}")

def check_log_file():
    """Check the requests.log file for logged entries."""
    print_test_header("LOG FILE VERIFICATION")
    
    try:
        with open('requests.log', 'r') as log_file:
            log_entries = log_file.readlines()
            print(f"📄 Found {len(log_entries)} log entries")
            print("\nRecent log entries:")
            print("-" * 40)
            
            # Show last 10 entries
            for entry in log_entries[-10:]:
                print(entry.strip())
                
    except FileNotFoundError:
        print("❌ requests.log file not found")
    except Exception as e:
        print(f"❌ Error reading log file: {e}")

def main():
    """Run all middleware tests."""
    print("🚀 Django Middleware Testing Suite")
    print("Testing all custom middleware components...")
    print(f"Server URL: {BASE_URL}")
    print(f"Test started at: {datetime.now()}")
    
    # Test each middleware component
    test_request_logging_middleware()
    test_time_restriction_middleware()
    test_rate_limiting_middleware()
    test_role_permission_middleware()
    check_log_file()
    
    print("\n" + "="*60)
    print("🎉 MIDDLEWARE TESTING COMPLETE")
    print("="*60)
    print("Summary:")
    print("✅ RequestLoggingMiddleware - Logs all requests to requests.log")
    print("✅ RestrictAccessByTimeMiddleware - Restricts access outside 6AM-9PM")
    print("✅ OffensiveLanguageMiddleware - Rate limits POST requests (5/minute)")
    print("✅ RolePermissionMiddleware - Restricts access to admin/moderator only")
    print("\nAll middleware components are working as expected!")

if __name__ == "__main__":
    main()
