#!/bin/bash

# Django Messaging App API Testing Script
# This script tests the JWT authentication and API endpoints

BASE_URL="http://127.0.0.1:8000"

echo "=== Django Messaging App API Testing ==="
echo "Base URL: $BASE_URL"
echo

# Create test users
echo "1. Creating test users..."
USER1_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/register/" \
  -H "Content-Type: application/json" \
  -d "{
    \"username\": \"testuser1\",
    \"email\": \"testuser1@example.com\",
    \"password\": \"testpassword123\",
    \"first_name\": \"Test\",
    \"last_name\": \"User1\",
    \"role\": \"guest\",
    \"phone_number\": \"+1234567890\"
  }")

USER2_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/register/" \
  -H "Content-Type: application/json" \
  -d "{
    \"username\": \"testuser2\",
    \"email\": \"testuser2@example.com\",
    \"password\": \"testpassword123\",
    \"first_name\": \"Test\",
    \"last_name\": \"User2\",
    \"role\": \"member\",
    \"phone_number\": \"+1234567891\"
  }")

echo "User 1: $USER1_RESPONSE"
echo "User 2: $USER2_RESPONSE"
echo

# Login as user1
echo "2. Logging in as testuser1..."
LOGIN_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/login/" \
  -H "Content-Type: application/json" \
  -d "{
    \"username\": \"testuser1\",
    \"password\": \"testpassword123\"
  }")

echo "Login Response: $LOGIN_RESPONSE"

# Extract access token
ACCESS_TOKEN=$(echo $LOGIN_RESPONSE | python -c "import json,sys; data=json.load(sys.stdin); print(data['tokens']['access'])")
USER_ID=$(echo $LOGIN_RESPONSE | python -c "import json,sys; data=json.load(sys.stdin); print(data['user']['user_id'])")

echo "Access Token: ${ACCESS_TOKEN:0:20}..."
echo "User ID: $USER_ID"
echo

# Test authenticated profile access
echo "3. Getting user profile..."
PROFILE_RESPONSE=$(curl -s -X GET "$BASE_URL/auth/profile/" \
  -H "Authorization: Bearer $ACCESS_TOKEN")

echo "Profile: $PROFILE_RESPONSE"
echo

# Test unauthenticated access (should fail)
echo "4. Testing unauthenticated access..."
UNAUTH_RESPONSE=$(curl -s -X GET "$BASE_URL/api/conversations/")
echo "Unauthenticated Access: $UNAUTH_RESPONSE"
echo

# List users
echo "5. Listing users..."
USERS_RESPONSE=$(curl -s -X GET "$BASE_URL/api/users/" \
  -H "Authorization: Bearer $ACCESS_TOKEN")

echo "Users: $USERS_RESPONSE"
echo

# Create a conversation
echo "6. Creating conversation..."
CONVERSATION_RESPONSE=$(curl -s -X POST "$BASE_URL/api/conversations/" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"participant_ids\": [\"$USER_ID\"]
  }")

echo "Conversation: $CONVERSATION_RESPONSE"

# Extract conversation ID
CONVERSATION_ID=$(echo $CONVERSATION_RESPONSE | python -c "import json,sys; data=json.load(sys.stdin); print(data['conversation_id'])")
echo "Conversation ID: $CONVERSATION_ID"
echo

# Send a message
echo "7. Sending message..."
MESSAGE_RESPONSE=$(curl -s -X POST "$BASE_URL/api/messages/" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"conversation\": \"$CONVERSATION_ID\",
    \"message_body\": \"Hello! This is a test message from curl script.\"
  }")

echo "Message: $MESSAGE_RESPONSE"

# Extract message ID
MESSAGE_ID=$(echo $MESSAGE_RESPONSE | python -c "import json,sys; data=json.load(sys.stdin); print(data['message_id'])")
echo "Message ID: $MESSAGE_ID"
echo

# Get conversations
echo "8. Getting conversations..."
CONVERSATIONS_RESPONSE=$(curl -s -X GET "$BASE_URL/api/conversations/" \
  -H "Authorization: Bearer $ACCESS_TOKEN")

echo "Conversations: $CONVERSATIONS_RESPONSE"
echo

# Get messages
echo "9. Getting messages..."
MESSAGES_RESPONSE=$(curl -s -X GET "$BASE_URL/api/messages/" \
  -H "Authorization: Bearer $ACCESS_TOKEN")

echo "Messages: $MESSAGES_RESPONSE"
echo

# Test filtering - messages by conversation
echo "10. Testing filtering - messages by conversation..."
FILTERED_MESSAGES=$(curl -s -X GET "$BASE_URL/api/messages/?conversation=$CONVERSATION_ID" \
  -H "Authorization: Bearer $ACCESS_TOKEN")

echo "Filtered Messages: $FILTERED_MESSAGES"
echo

# Test search - messages containing "test"
echo "11. Testing search - messages containing 'test'..."
SEARCH_MESSAGES=$(curl -s -X GET "$BASE_URL/api/messages/?search=test" \
  -H "Authorization: Bearer $ACCESS_TOKEN")

echo "Search Results: $SEARCH_MESSAGES"
echo

# Test pagination
echo "12. Testing pagination..."
PAGINATED_MESSAGES=$(curl -s -X GET "$BASE_URL/api/messages/?page=1&page_size=5" \
  -H "Authorization: Bearer $ACCESS_TOKEN")

echo "Paginated Messages: $PAGINATED_MESSAGES"
echo

# Update message
echo "13. Updating message..."
UPDATE_RESPONSE=$(curl -s -X PUT "$BASE_URL/api/messages/$MESSAGE_ID/" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"conversation\": \"$CONVERSATION_ID\",
    \"message_body\": \"Updated message content from curl script.\"
  }")

echo "Update Response: $UPDATE_RESPONSE"
echo

# Test token refresh
echo "14. Testing token refresh..."
REFRESH_TOKEN=$(echo $LOGIN_RESPONSE | python -c "import json,sys; data=json.load(sys.stdin); print(data['tokens']['refresh'])")

REFRESH_RESPONSE=$(curl -s -X POST "$BASE_URL/auth/token/refresh/" \
  -H "Content-Type: application/json" \
  -d "{
    \"refresh\": \"$REFRESH_TOKEN\"
  }")

echo "Token Refresh: $REFRESH_RESPONSE"
echo

echo "=== API Testing Complete ==="
