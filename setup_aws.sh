#!/bin/bash

# WhatsApp Bot Neonize Setup Script for Ubuntu 22.04+ (AWS EC2)
# Author: Antigravity AI

echo "Updating system..."
sudo apt update && sudo apt upgrade -y

echo "Installing Python and dependencies..."
sudo apt install -y python3-pip python3-venv git build-essential

echo "Installing Go (required for Neonize)..."
# Neonize uses Go under the hood
sudo apt install -y golang-go

echo "Creating Python Virtual Environment..."
python3 -m venv venv
source venv/bin/activate

echo "Installing Python dependencies..."
pip install --upgrade pip
pip install neonize python-dotenv

echo "----------------------------------------"
echo "Setup Complete!"
echo "----------------------------------------"
echo "Cara menjalankan bot:"
echo "1. Pastikan Anda berada di direktori project"
echo "2. Jalankan perintah: source venv/bin/activate"
echo "3. Jalankan bot: python3 main.py"
echo "4. Scan QR code yang muncul di terminal menggunakan WhatsApp Anda"
echo ""
echo "Catatan: Gunakan 'tmux' atau 'screen' agar bot tetap berjalan setelah SSH ditutup."
echo "Contoh: tmux new -s wabot"
echo "----------------------------------------"
