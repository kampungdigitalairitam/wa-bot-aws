#!/bin/bash

# WhatsApp Bot Neonize Setup Script for AWS (Ubuntu or Amazon Linux)
# Author: Antigravity AI

echo "Detecting OS and Package Manager..."

if command -v apt-get &> /dev/null; then
    echo "OS Detected: Ubuntu/Debian"
    sudo apt-get update && sudo apt-get upgrade -y
    sudo apt-get install -y python3-pip python3-venv git build-essential golang-go
    
    # Check if python3 version is >= 3.10
    PY_VER=$(python3 -c 'import sys; print(sys.version_info >= (3, 10))')
    if [ "$PY_VER" == "False" ]; then
        echo "Installing Python 3.10 for Ubuntu..."
        sudo add-apt-repository ppa:deadsnakes/ppa -y
        sudo apt-get update
        sudo apt-get install -y python3.10 python3.10-venv python3.10-dev
        PYTHON_CMD="python3.10"
    else
        PYTHON_CMD="python3"
    fi

elif command -v yum &> /dev/null; then
    echo "OS Detected: Amazon Linux/RHEL/CentOS"
    sudo yum update -y
    sudo yum groupinstall "Development Tools" -y
    sudo yum install -y git golang
    
    # Amazon Linux usually has python3.11 or python3.9
    if command -v python3.11 &> /dev/null; then
        PYTHON_CMD="python3.11"
    elif command -v python3.10 &> /dev/null; then
        PYTHON_CMD="python3.10"
    else
        echo "Installing Python 3.11 for Amazon Linux..."
        sudo yum install -y python3.11 python3.11-devel python3.11-pip
        PYTHON_CMD="python3.11"
    fi
else
    echo "Could not detect package manager (apt or yum). Please install dependencies manually."
    exit 1
fi

echo "Using Python command: $PYTHON_CMD"

echo "Creating Python Virtual Environment..."
rm -rf venv # Clean up old venv if exists
$PYTHON_CMD -m venv venv
source venv/bin/activate

echo "Installing/Upgrading Pip..."
pip install --upgrade pip

echo "Installing WhatsApp Bot dependencies (neonize, python-dotenv)..."
pip install neonize python-dotenv

echo "----------------------------------------"
echo "Setup Complete!"
echo "----------------------------------------"
echo "Cara menjalankan bot:"
echo "1. Pastikan Anda berada di direktori project"
echo "2. Jalankan perintah: source venv/bin/activate"
echo "3. Jalankan bot: python3 main.py"
echo "4. Scan QR code yang muncul di terminal"
echo "----------------------------------------"
