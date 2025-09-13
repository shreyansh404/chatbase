#!/bin/bash

# Setup script for ChatBase WhatsApp Bot

echo "Setting up ChatBase WhatsApp Bot..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.7 or higher."
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Copy environment file
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
    echo "Please edit .env file with your Twilio credentials"
else
    echo ".env file already exists"
fi

echo "Setup completed!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your Twilio credentials"
echo "2. Run 'source venv/bin/activate' to activate virtual environment"
echo "3. Run 'python app.py' to start the bot"
echo "4. Configure your Twilio webhook URL to point to your server/ngrok URL + /webhook"