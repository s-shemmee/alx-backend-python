#!/usr/bin/env python3
"""
Django Messaging App API Testing Script
Tests JWT authentication and API endpoints
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

class APITester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.access_token = None
        self.user_id = None
        self.conversation_id = None
        self.message_id = None
        
    def print_response(self, response, title):
        """Print formatted response"""
        print(f"\n{title}")
        print(f"Status: {response.status_code}")
        try:
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        except:
            print(f"Response: {response.text}")
    
    def register_user(self, username, email, password, first_name, last_name, role="guest", phone=None):
        """Register a new user"""
        data = {
            "username": username,
            "email": email,
            "password": password,
            "first_name": first_name,
            "last_name": last_name,
            "role": role
        }
        if phone:
            data["phone_number"] = phone
            
        response = self.session.post(f"{self.base_url}/auth/register/", json=data)
        return response
    
    def login(self, username, password):
        """Login and store tokens"""
        data = {
            "username": username,
            "password": password
        }
        response = self.session.post(f"{self.base_url}/auth/login/", json=data)
        
        if response.status_code == 200:
            data = response.json()
            self.access_token = data['tokens']['access']
            self.user_id = data['user']['user_id']
            # Set authorization header for future requests
            self.session.headers.update({
                'Authorization': f'Bearer {self.access_token}'
            })
        
        return response
    
    def get_profile(self):
        """Get user profile"""
        return self.session.get(f"{self.base_url}/auth/profile/")
    
    def list_users(self):
        """List all users"""
        return self.session.get(f"{self.base_url}/api/users/")
    
    def create_conversation(self, participant_ids):
        """Create a new conversation"""
        data = {"participant_ids": participant_ids}
        response = self.session.post(f"{self.base_url}/api/conversations/", json=data)
        
        if response.status_code == 201:
            self.conversation_id = response.json()['conversation_id']
        
        return response
    
    def list_conversations(self):
        """List conversations"""
        return self.session.get(f"{self.base_url}/api/conversations/")
    
    def send_message(self, conversation_id, message_body):
        """Send a message"""
        data = {
            "conversation": conversation_id,
            "message_body": message_body
        }
        response = self.session.post(f"{self.base_url}/api/messages/", json=data)
        
        if response.status_code == 201:
            self.message_id = response.json()['message_id']
        
        return response
    
    def list_messages(self, **params):
        """List messages with optional filters"""
        return self.session.get(f"{self.base_url}/api/messages/", params=params)
    
    def update_message(self, message_id, conversation_id, message_body):
        """Update a message"""
        data = {
            "conversation": conversation_id,
            "message_body": message_body
        }
        return self.session.put(f"{self.base_url}/api/messages/{message_id}/", json=data)
    
    def test_unauthorized_access(self):
        """Test access without authentication"""
        # Create a new session without auth headers
        temp_session = requests.Session()
        return temp_session.get(f"{self.base_url}/api/conversations/")
    
    def run_full_test(self):
        """Run complete API test suite"""
        print("=== Django Messaging App API Testing ===")
        print(f"Base URL: {self.base_url}")
        
        # 1. Register users
        print("\n1. Registering test users...")
        user1_response = self.register_user(
            "apiuser1", "apiuser1@example.com", "testpassword123",
            "API", "User1", "guest", "+1234567890"
        )
        self.print_response(user1_response, "User 1 Registration")
        
        user2_response = self.register_user(
            "apiuser2", "apiuser2@example.com", "testpassword123",
            "API", "User2", "member", "+1234567891"
        )
        self.print_response(user2_response, "User 2 Registration")
        
        # 2. Login
        print("\n2. Logging in as apiuser1...")
        login_response = self.login("apiuser1", "testpassword123")
        self.print_response(login_response, "Login")
        
        if login_response.status_code != 200:
            print("Login failed! Cannot continue with authenticated tests.")
            return
        
        # 3. Get profile
        print("\n3. Getting user profile...")
        profile_response = self.get_profile()
        self.print_response(profile_response, "User Profile")
        
        # 4. Test unauthorized access
        print("\n4. Testing unauthorized access...")
        unauth_response = self.test_unauthorized_access()
        self.print_response(unauth_response, "Unauthorized Access")
        
        # 5. List users
        print("\n5. Listing users...")
        users_response = self.list_users()
        self.print_response(users_response, "Users List")
        
        # 6. Create conversation
        print("\n6. Creating conversation...")
        conversation_response = self.create_conversation([self.user_id])
        self.print_response(conversation_response, "Create Conversation")
        
        if not self.conversation_id:
            print("Failed to create conversation! Cannot continue with message tests.")
            return
        
        # 7. Send message
        print("\n7. Sending message...")
        message_response = self.send_message(
            self.conversation_id,
            "Hello! This is a test message from Python script."
        )
        self.print_response(message_response, "Send Message")
        
        # 8. List conversations
        print("\n8. Listing conversations...")
        conversations_response = self.list_conversations()
        self.print_response(conversations_response, "Conversations List")
        
        # 9. List messages
        print("\n9. Listing messages...")
        messages_response = self.list_messages()
        self.print_response(messages_response, "Messages List")
        
        # 10. Test filtering - messages by conversation
        print("\n10. Testing filtering - messages by conversation...")
        filtered_response = self.list_messages(conversation=self.conversation_id)
        self.print_response(filtered_response, "Filtered Messages")
        
        # 11. Test search
        print("\n11. Testing search - messages containing 'test'...")
        search_response = self.list_messages(search="test")
        self.print_response(search_response, "Search Results")
        
        # 12. Test pagination
        print("\n12. Testing pagination...")
        paginated_response = self.list_messages(page=1, page_size=5)
        self.print_response(paginated_response, "Paginated Messages")
        
        # 13. Update message
        if self.message_id:
            print("\n13. Updating message...")
            update_response = self.update_message(
                self.message_id,
                self.conversation_id,
                "Updated message content from Python script."
            )
            self.print_response(update_response, "Update Message")
        
        # 14. Test date filtering
        print("\n14. Testing date filtering...")
        today = datetime.now().strftime("%Y-%m-%dT00:00:00Z")
        date_filtered = self.list_messages(sent_after=today)
        self.print_response(date_filtered, "Date Filtered Messages")
        
        print("\n=== API Testing Complete ===")

def main():
    tester = APITester(BASE_URL)
    tester.run_full_test()

if __name__ == "__main__":
    main()
