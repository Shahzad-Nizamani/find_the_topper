#!/bin/bash

# Exit immediately if a command fails
set -e

# Install Chrome
echo "📦 Installing Google Chrome..."
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt update
apt install -y ./google-chrome-stable_current_amd64.deb

# Detect Chrome version (e.g., 125.0.6422.141)
CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+\.\d+')
echo "🔍 Detected Chrome version: $CHROME_VERSION"

# Download matching Chromedriver
echo "📥 Downloading ChromeDriver for version $CHROME_VERSION..."
wget https://storage.googleapis.com/chrome-for-testing-public/$CHROME_VERSION/linux64/chromedriver-linux64.zip

# Unzip and install Chromedriver
unzip chromedriver-linux64.zip
chmod +x chromedriver-linux64/chromedriver
mv chromedriver-linux64/chromedriver /usr/local/bin/chromedriver

# Confirm installed
echo "✅ ChromeDriver installed at /usr/local/bin/chromedriver"
