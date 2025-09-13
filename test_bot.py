#!/usr/bin/env python3
"""
Test script for WhatsApp Bot
"""

import requests
import json
import time


def test_webhook_locally():
    """Test the webhook endpoint locally"""
    
    # Test data mimicking Twilio's webhook request
    test_data = {
        'Body': 'hello',
        'From': 'whatsapp:+1234567890',
        'To': 'whatsapp:+14155238886',
        'MessageSid': 'test_message_id',
        'AccountSid': 'test_account_sid'
    }
    
    try:
        response = requests.post('http://localhost:5000/webhook', data=test_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        # Test different commands
        test_commands = ['help', 'about', 'time', 'weather', 'random message']
        
        for command in test_commands:
            test_data['Body'] = command
            response = requests.post('http://localhost:5000/webhook', data=test_data)
            print(f"\nCommand: {command}")
            print(f"Response: {response.text}")
            time.sleep(1)
            
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the bot. Make sure it's running on localhost:5000")
    except Exception as e:
        print(f"Error: {str(e)}")


def test_health_endpoint():
    """Test the health check endpoint"""
    try:
        response = requests.get('http://localhost:5000/health')
        print(f"Health Check Status: {response.status_code}")
        print(f"Health Response: {response.json()}")
    except Exception as e:
        print(f"Health check failed: {str(e)}")


def test_send_message():
    """Test sending a message (requires valid Twilio credentials)"""
    test_message = {
        'to': 'whatsapp:+1234567890',  # Replace with your WhatsApp number
        'message': 'Test message from ChatBase Bot!'
    }
    
    try:
        response = requests.post(
            'http://localhost:5000/send', 
            json=test_message,
            headers={'Content-Type': 'application/json'}
        )
        print(f"Send Message Status: {response.status_code}")
        print(f"Send Response: {response.json()}")
    except Exception as e:
        print(f"Send message failed: {str(e)}")


if __name__ == '__main__':
    print("Testing ChatBase WhatsApp Bot...")
    print("=" * 50)
    
    # Test health endpoint first
    print("1. Testing health endpoint...")
    test_health_endpoint()
    
    print("\n2. Testing webhook locally...")
    test_webhook_locally()
    
    print("\n3. Testing send message endpoint...")
    print("Note: This requires valid Twilio credentials")
    test_send_message()
    
    print("\nTesting completed!")