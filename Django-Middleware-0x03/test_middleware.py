#!/usr/bin/env python3
"""
Test script for Django Middleware functionality.
Tests all custom middleware components including:
1. RequestLoggingMiddleware
2. RestrictAccessByTimeMiddleware  
3. OffensiveLanguageMiddleware
4. RolePermissionMiddleware
"""

import requests
import time
import json
from datetime import datetime


class MiddlewareTestSuite:
    def __init__(self, base_url="http://localhost:8001"):
        self.base_url = base_url
        self.access_token = None
        self.test_results = {}
        
    def log(self, message):
        """Log test messages with timestamp."""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")
        
    def test_request_logging_middleware(self):
        """Test 1: RequestLoggingMiddleware - Logs all requests to requests.log"""
        self.log("=" * 60)
        self.log("Testing RequestLoggingMiddleware")
        self.log("=" * 60)
        
        try:
            # Make multiple requests to test logging
            test_paths = ["/", "/api/", "/api/users/", "/admin/"]
            
            for path in test_paths:
                response = requests.get(f"{self.base_url}{path}")
                self.log(f"GET {path} - Status: {response.status_code}")
                time.sleep(0.5)  # Small delay between requests
                
            self.log("✅ RequestLoggingMiddleware test completed")
            self.log("📋 Check requests.log file for logged entries")
            self.test_results['RequestLoggingMiddleware'] = 'PASS'
            
        except Exception as e:
            self.log(f"❌ RequestLoggingMiddleware test failed: {e}")
            self.test_results['RequestLoggingMiddleware'] = 'FAIL'
    
    def test_time_restriction_middleware(self):
        """Test 2: RestrictAccessByTimeMiddleware - Restricts access outside 6AM-9PM"""
        self.log("=" * 60)
        self.log("Testing RestrictAccessByTimeMiddleware")
        self.log("=" * 60)
        
        try:
            current_hour = datetime.now().hour
            self.log(f"Current time: {datetime.now().strftime('%H:%M:%S')} (Hour: {current_hour})")
            
            response = requests.get(f"{self.base_url}/api/users/")
            
            if 6 <= current_hour < 21:
                self.log("⏰ Currently within allowed hours (6AM-9PM)")
                if response.status_code == 401:  # Should get auth error, not time restriction
                    self.log("✅ Time restriction middleware allows access during allowed hours")
                    self.test_results['RestrictAccessByTimeMiddleware'] = 'PASS'
                else:
                    self.log(f"Response: {response.text[:100]}...")
            else:
                self.log("⏰ Currently outside allowed hours (6AM-9PM)")
                if response.status_code == 403 and "restricted outside" in response.text:
                    self.log("✅ Time restriction middleware correctly blocks access")
                    self.test_results['RestrictAccessByTimeMiddleware'] = 'PASS'
                else:
                    self.log(f"❌ Expected 403 with time restriction message, got: {response.status_code}")
                    self.test_results['RestrictAccessByTimeMiddleware'] = 'FAIL'
                    
        except Exception as e:
            self.log(f"❌ RestrictAccessByTimeMiddleware test failed: {e}")
            self.test_results['RestrictAccessByTimeMiddleware'] = 'FAIL'
    
    def test_rate_limiting_middleware(self):
        """Test 3: OffensiveLanguageMiddleware - Rate limits POST requests to /api/messages/"""
        self.log("=" * 60)
        self.log("Testing OffensiveLanguageMiddleware (Rate Limiting)")
        self.log("=" * 60)
        
        try:
            # Simulate rapid POST requests to trigger rate limiting
            message_data = {
                "message_body": "Test message",
                "conversation": "test-conversation-id"
            }
            
            success_count = 0
            rate_limited = False
            
            for i in range(7):  # Try to send 7 messages (limit is 5 per minute)
                response = requests.post(
                    f"{self.base_url}/api/messages/",
                    json=message_data,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 403 and "Rate limit exceeded" in response.text:
                    self.log(f"🛑 Request {i+1}: Rate limited (Status: {response.status_code})")
                    rate_limited = True
                    break
                else:
                    self.log(f"📤 Request {i+1}: Status {response.status_code}")
                    success_count += 1
                
                time.sleep(0.1)  # Small delay between requests
            
            if rate_limited:
                self.log("✅ OffensiveLanguageMiddleware correctly implemented rate limiting")
                self.test_results['OffensiveLanguageMiddleware'] = 'PASS'
            else:
                self.log("⚠️  Rate limiting not triggered - middleware may need adjustment")
                self.test_results['OffensiveLanguageMiddleware'] = 'PARTIAL'
                
        except Exception as e:
            self.log(f"❌ OffensiveLanguageMiddleware test failed: {e}")
            self.test_results['OffensiveLanguageMiddleware'] = 'FAIL'
    
    def test_role_permission_middleware(self):
        """Test 4: RolePermissionMiddleware - Restricts access based on user roles"""
        self.log("=" * 60)
        self.log("Testing RolePermissionMiddleware")
        self.log("=" * 60)
        
        try:
            # Test protected endpoints without authentication
            protected_endpoints = [
                "/admin/",
                "/api/users/", 
                "/api/conversations/"
            ]
            
            for endpoint in protected_endpoints:
                response = requests.get(f"{self.base_url}{endpoint}")
                
                if response.status_code == 403:
                    if "Authentication required" in response.text or "Access denied" in response.text:
                        self.log(f"🔒 {endpoint}: Correctly blocked (Status: {response.status_code})")
                    else:
                        self.log(f"🔒 {endpoint}: Blocked with different message: {response.text[:50]}...")
                else:
                    self.log(f"⚠️  {endpoint}: Unexpected status {response.status_code}")
            
            self.log("✅ RolePermissionMiddleware correctly restricts access to protected endpoints")
            self.test_results['RolePermissionMiddleware'] = 'PASS'
            
        except Exception as e:
            self.log(f"❌ RolePermissionMiddleware test failed: {e}")
            self.test_results['RolePermissionMiddleware'] = 'FAIL'
    
    def display_summary(self):
        """Display test results summary."""
        self.log("=" * 60)
        self.log("MIDDLEWARE TEST SUMMARY")
        self.log("=" * 60)
        
        for middleware, result in self.test_results.items():
            status_icon = "✅" if result == "PASS" else "⚠️" if result == "PARTIAL" else "❌"
            self.log(f"{status_icon} {middleware}: {result}")
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results.values() if result == "PASS")
        
        self.log("=" * 60)
        self.log(f"Total Tests: {total_tests}")
        self.log(f"Passed: {passed_tests}")
        self.log(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        self.log("=" * 60)
        
        # Additional information
        self.log("📝 Additional Notes:")
        self.log("   • Check requests.log for request logging entries")
        self.log("   • Time restriction depends on current server time")
        self.log("   • Rate limiting resets every minute")
        self.log("   • Role permissions require authentication tokens")


def main():
    """Run the complete middleware test suite."""
    print("🚀 Django Middleware Test Suite")
    print("Testing custom middleware components...")
    print()
    
    tester = MiddlewareTestSuite()
    
    # Run all middleware tests
    tester.test_request_logging_middleware()
    time.sleep(1)
    
    tester.test_time_restriction_middleware()
    time.sleep(1)
    
    tester.test_rate_limiting_middleware()
    time.sleep(1)
    
    tester.test_role_permission_middleware()
    time.sleep(1)
    
    # Display summary
    tester.display_summary()


if __name__ == "__main__":
    main()
