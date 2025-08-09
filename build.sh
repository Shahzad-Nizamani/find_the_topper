#!/bin/bash

# Exit immediately if a command fails
set -e

# Install Chrome
echo "📦 Installing Google Chrome..."
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt update
apt install -y ./google-chrome-stable_current_amd64.deb

# Confirm Chrome version
google-chrome --version
echo "✅ Google Chrome installed successfully"
