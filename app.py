#!/usr/bin/env python3
"""
WhatsApp Chatbot using Twilio API
A simple chatbot that can respond to WhatsApp messages
"""

import os
import logging
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Twilio configuration
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER', 'whatsapp:+14155238886')

# Initialize Twilio client
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN) if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN else None


class WhatsAppBot:
    """WhatsApp Bot class to handle message processing"""
    
    def __init__(self):
        self.commands = {
            'hello': self.handle_hello,
            'hi': self.handle_hello,
            'help': self.handle_help,
            'about': self.handle_about,
            'time': self.handle_time,
            'weather': self.handle_weather,
        }
    
    def process_message(self, message_body, sender_number):
        """Process incoming message and return appropriate response"""
        message_body = message_body.lower().strip()
        
        # Check for commands
        for command, handler in self.commands.items():
            if message_body.startswith(command):
                return handler(message_body, sender_number)
        
        # Default response for unrecognized messages
        return self.handle_default(message_body, sender_number)
    
    def handle_hello(self, message, sender):
        """Handle hello/hi messages"""
        return "Hello! 👋 Welcome to ChatBase WhatsApp Bot. Type 'help' to see available commands."
    
    def handle_help(self, message, sender):
        """Handle help command"""
        help_text = """
🤖 *ChatBase Bot Commands:*

• *hello/hi* - Greet the bot
• *help* - Show this help message
• *about* - Learn about this bot
• *time* - Get current time
• *weather* - Get weather info (coming soon)

Just type any command to get started!
        """
        return help_text.strip()
    
    def handle_about(self, message, sender):
        """Handle about command"""
        return """
🤖 *About ChatBase WhatsApp Bot*

This is a simple WhatsApp chatbot built with Python, Flask, and Twilio API. 

Features:
• Responds to basic commands
• Easy to extend with new functionality
• Built with modern Python frameworks

Created with ❤️ using Twilio WhatsApp API
        """.strip()
    
    def handle_time(self, message, sender):
        """Handle time command"""
        from datetime import datetime
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"🕐 Current time: {current_time}"
    
    def handle_weather(self, message, sender):
        """Handle weather command (placeholder)"""
        return "🌤️ Weather feature is coming soon! Stay tuned for updates."
    
    def handle_default(self, message, sender):
        """Handle unrecognized messages"""
        return """
I didn't understand that message. 🤔

Type *'help'* to see what I can do, or try:
• hello
• about  
• time
        """.strip()


# Initialize bot
bot = WhatsAppBot()


@app.route('/webhook', methods=['POST'])
def webhook():
    """Handle incoming WhatsApp messages"""
    try:
        # Get message details from Twilio
        incoming_msg = request.values.get('Body', '').strip()
        sender_number = request.values.get('From', '')
        
        logger.info(f"Received message from {sender_number}: {incoming_msg}")
        
        # Process message through bot
        response_text = bot.process_message(incoming_msg, sender_number)
        
        # Create Twilio response
        resp = MessagingResponse()
        resp.message(response_text)
        
        logger.info(f"Sending response: {response_text}")
        
        return str(resp)
    
    except Exception as e:
        logger.error(f"Error processing webhook: {str(e)}")
        resp = MessagingResponse()
        resp.message("Sorry, I encountered an error. Please try again later.")
        return str(resp)


@app.route('/send', methods=['POST'])
def send_message():
    """Send a message via WhatsApp (for testing/admin use)"""
    if not twilio_client:
        return {"error": "Twilio client not configured"}, 400
    
    try:
        to_number = request.json.get('to')
        message_body = request.json.get('message')
        
        if not to_number or not message_body:
            return {"error": "Missing 'to' or 'message' in request"}, 400
        
        # Send message
        message = twilio_client.messages.create(
            body=message_body,
            from_=TWILIO_WHATSAPP_NUMBER,
            to=to_number
        )
        
        logger.info(f"Message sent to {to_number}: {message.sid}")
        
        return {"success": True, "message_sid": message.sid}
    
    except Exception as e:
        logger.error(f"Error sending message: {str(e)}")
        return {"error": str(e)}, 500


@app.route('/health')
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "ChatBase WhatsApp Bot"}


@app.route('/')
def index():
    """Home page"""
    return """
    <h1>ChatBase WhatsApp Bot</h1>
    <p>Bot is running and ready to receive messages!</p>
    <p>Configure your Twilio webhook URL to point to: <code>/webhook</code></p>
    <ul>
        <li><a href="/health">Health Check</a></li>
    </ul>
    """


if __name__ == '__main__':
    # Check if Twilio credentials are configured
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
        logger.warning("Twilio credentials not found. Bot will run in demo mode.")
        logger.warning("Set TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN environment variables.")
    
    # Run the Flask app
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting ChatBase WhatsApp Bot on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)