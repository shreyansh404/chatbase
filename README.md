# ChatBase - WhatsApp Chatbot

A sophisticated WhatsApp chatbot built with Python, Flask, and Twilio API. This bot can handle multiple commands and can be easily extended with new functionality.

## Features

- 🤖 **Smart Command Processing**: Handles multiple commands with intelligent responses
- 📱 **WhatsApp Integration**: Uses Twilio API for reliable WhatsApp messaging
- 🚀 **Easy Deployment**: Simple setup with Flask and configurable environment
- 🔧 **Extensible**: Easy to add new commands and features
- 📝 **Comprehensive Logging**: Built-in logging for monitoring and debugging
- 🧪 **Testing Suite**: Includes testing utilities for development

## Available Commands

| Command | Description |
|---------|-------------|
| `hello` or `hi` | Greet the bot |
| `help` | Show available commands |
| `about` | Learn about the bot |
| `time` | Get current time |
| `weather` | Weather information (coming soon) |

## Prerequisites

- Python 3.7 or higher
- Twilio account with WhatsApp API access
- ngrok (for local development) or a hosted server

## Quick Setup

### 1. Clone and Setup

```bash
git clone https://github.com/shreyansh404/chatbase.git
cd chatbase
./setup.sh
```

### 2. Configure Environment

Edit the `.env` file with your Twilio credentials:

```bash
# Twilio credentials (get these from https://console.twilio.com)
TWILIO_ACCOUNT_SID=your_twilio_account_sid_here
TWILIO_AUTH_TOKEN=your_twilio_auth_token_here

# WhatsApp number provided by Twilio
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886

# Your verified WhatsApp number for testing
YOUR_WHATSAPP_NUMBER=whatsapp:+1234567890
```

### 3. Get Twilio WhatsApp Credentials

1. Sign up at [Twilio Console](https://console.twilio.com)
2. Go to Programmable Messaging > WhatsApp
3. Follow the WhatsApp Sandbox setup
4. Get your Account SID and Auth Token
5. Note your Twilio WhatsApp number

### 4. Run the Bot

```bash
# Activate virtual environment
source venv/bin/activate

# Start the bot
python app.py
```

The bot will start on `http://localhost:5000`

### 5. Setup Webhook (for Development)

For local development, use ngrok to expose your local server:

```bash
# Install ngrok: https://ngrok.com/download
ngrok http 5000
```

Copy the HTTPS URL and configure it in your Twilio Console:
- Go to Programmable Messaging > WhatsApp > Sandbox
- Set webhook URL to: `https://your-ngrok-url.ngrok.io/webhook`

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page |
| `/webhook` | POST | WhatsApp webhook (for Twilio) |
| `/send` | POST | Send message programmatically |
| `/health` | GET | Health check |

## Testing

Run the test suite to verify everything is working:

```bash
python test_bot.py
```

This will test:
- Health endpoint
- Webhook functionality
- Message sending capability

## Development

### Adding New Commands

1. Open `app.py`
2. Add your command to the `commands` dictionary in `WhatsAppBot.__init__`
3. Create a handler method following the pattern `handle_your_command`

Example:
```python
def handle_joke(self, message, sender):
    """Handle joke command"""
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "Why did the scarecrow win an award? He was outstanding in his field!"
    ]
    return random.choice(jokes)
```

### Configuration

The bot uses environment variables for configuration. See `config.py` for all available options.

## Deployment

### Heroku Deployment

1. Create a `Procfile`:
```
web: gunicorn app:app
```

2. Deploy to Heroku:
```bash
heroku create your-app-name
heroku config:set TWILIO_ACCOUNT_SID=your_sid
heroku config:set TWILIO_AUTH_TOKEN=your_token
git push heroku main
```

3. Update Twilio webhook URL to: `https://your-app-name.herokuapp.com/webhook`

### Other Platforms

The bot is a standard Flask application and can be deployed to:
- AWS Lambda + API Gateway
- Google Cloud Run
- DigitalOcean App Platform
- Railway
- Any VPS with Python support

## Project Structure

```
chatbase/
├── app.py              # Main application file
├── config.py           # Configuration management
├── test_bot.py         # Testing utilities
├── setup.sh            # Setup script
├── requirements.txt    # Python dependencies
├── .env.example        # Environment template
├── .gitignore         # Git ignore rules
└── README.md          # This file
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is open source and available under the [MIT License](LICENSE).

## Support

- 📚 [Twilio WhatsApp API Documentation](https://www.twilio.com/docs/whatsapp)
- 🐛 [Report Issues](https://github.com/shreyansh404/chatbase/issues)
- 💬 [Discussions](https://github.com/shreyansh404/chatbase/discussions)

## Troubleshooting

### Common Issues

1. **"Twilio credentials not found"**
   - Make sure your `.env` file has the correct credentials
   - Verify your Twilio Account SID and Auth Token

2. **"Webhook not receiving messages"**
   - Check that your webhook URL is configured correctly in Twilio Console
   - Ensure your server is accessible from the internet (use ngrok for local development)

3. **"Bot not responding"**
   - Check the logs for any errors
   - Verify your WhatsApp number is verified in the Twilio Sandbox

### Debug Mode

Enable debug mode by setting `FLASK_DEBUG=True` in your `.env` file for detailed error messages.

---

Made with ❤️ using Python, Flask, and Twilio API
