#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

# Update package list
apt-get update

# Install dependencies for Chrome
apt-get install -y wget unzip xvfb libxi6 libgconf-2-4 libnss3 libasound2 fonts-liberation libappindicator3-1 xdg-utils libu2f-udev

# Install Google Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -i google-chrome-stable_current_amd64.deb || apt-get -fy install

# Get the full Chrome version
CHROME_VERSION=$(google-chrome --version | grep -oP '\d+\.\d+\.\d+\.\d+')

# Download matching ChromeDriver (Chrome for Testing format)
wget https://storage.googleapis.com/chrome-for-testing-public/${CHROME_VERSION}/linux64/chromedriver-linux64.zip

# Extract and install chromedriver
unzip chromedriver-linux64.zip
mv chromedriver-linux64/chromedriver /usr/local/bin/chromedriver
chmod +x /usr/local/bin/chromedriver
